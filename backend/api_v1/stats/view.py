import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.doctors.roles import Role
from api_v1.workload.workload import WorkloadType
from api_v1.doctors.crud import get_doctors_confident
from api_v1.reports.crud import get_total_for_week
from api_v1.events.crud import get_events
from .schemas import Stats
from auth import authenticate, oauth2_scheme
from authorize import authorize
from logic.date_decomposition import date_to_year_and_week_number
from logic.scheduler import reconsider_schedule
from core.models import db_helper
from . import crud

router = APIRouter(tags=["Stats"])


@router.get("/", response_model=Stats)
async def get_stats(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):

    user = await authenticate(token, session)
    authorize(user, Role.DOCTOR)

    today = datetime.date.today()
    year, week_number = date_to_year_and_week_number(today)

    doctors = await get_doctors_confident(session)

    week_start = today + datetime.timedelta(days=-today.weekday())
    week_end = week_start + datetime.timedelta(days=6)

    current_progress = {}

    for workload_type in WorkloadType:
        total = await get_total_for_week(week_start, week_end, workload_type, session)
        current_progress[workload_type] = total 

    events = get_events(session=session, date_from=week_start, date_to=week_end)

    # FUCKING MAGIC HAPPENS
    predictions_this_week = {}

    recommendations = reconsider_schedule(
        doctors,
        current_progress,
        predictions_this_week,
        events)

    today += datetime.timedelta(days=-today.weekday())

    report = await crud.get_total_for_week(today, today + datetime.timedelta(days=6), workload_type, session)

    return report
