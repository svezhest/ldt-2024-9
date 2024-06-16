from collections import defaultdict
import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.doctors.roles import Role
from api_v1.schedule.schemas import EventType, ScheduleEvent, ShiftingType
from api_v1.workload.workload import WorkloadType, proportions
from api_v1.doctors.crud import get_doctors_confident
from api_v1.reports.crud import get_total_for_week
from api_v1.events.crud import get_events
from .schemas import Stats, WorkloadTypeStats
from auth import authenticate, oauth2_scheme
from authorize import authorize
from logic.date_decomposition import date_to_year_and_week_number
from logic.scheduler import reconsider_schedule
from logic.predict import predict
from core.models import db_helper

router = APIRouter(tags=["Stats"])


@router.get("/", response_model=Stats)
async def get_stats(
        date: datetime.date | None = None,
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):

    user = await authenticate(token, session)
    authorize(user, Role.DOCTOR)

    if date is None:
        date = datetime.date.today()
    
    year, week_number = date_to_year_and_week_number(date)

    doctors = await get_doctors_confident(session)

    week_start = date + datetime.timedelta(days=-date.weekday())
    week_end = week_start + datetime.timedelta(days=6)

    current_progress = defaultdict(int)
    expected_this_week = defaultdict(int)

    _events = await get_events(session=session, date_from=week_start, date_to=week_end)
    events = _events.events

    for workload_type in WorkloadType:
        total = await get_total_for_week(week_start, week_end, workload_type, session)
        current_progress[workload_type] = total

        for doctor in doctors:
            assumed_hours = doctor.hours_per_week
            corrected_hours = assumed_hours

            if doctor.shifting_type == ShiftingType.TWO_TWO:
                estimated_day_hours = 12
            else:
                if doctor.hours_per_week == 40:
                    estimated_day_hours = 8
                else:
                    estimated_day_hours = 6

            for e in events:
                if e.event_type == EventType.OVERTIME:
                    corrected_hours += estimated_day_hours
                else:
                    corrected_hours -= estimated_day_hours
                # TODO: consider redirecting doctor here

            for (_workload_type, proportion) in proportions[doctor.skills.primary_skill]:
                expected_this_week[_workload_type] += corrected_hours * proportion

    predictions_this_week = predict(year, week_number)

    recommendations = reconsider_schedule(
        doctors,
        current_progress,
        expected_this_week,
        predictions_this_week,
        events)

    date += datetime.timedelta(days=-date.weekday())

    return Stats(stats=[
        WorkloadTypeStats(
            workload_type=_workload_type,
            done=current_progress[_workload_type],
            done_prediction=expected_this_week[_workload_type],
            needed_prediction=predictions_this_week[_workload_type],
            recommendation=recommendation
        ) for _workload_type in WorkloadType for recommendation in recommendations[_workload_type]
    ])
