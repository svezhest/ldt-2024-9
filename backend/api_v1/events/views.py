import datetime
import time
from fastapi import APIRouter, HTTPException, status, Depends
import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.doctors.roles import Role
from api_v1.schedule.schemas import DaySchedule, Events, Interval, Schedule, ScheduleEvent, StartHours
from auth import authenticate, oauth2_scheme
from authorize import authorize
from core.models import db_helper
from . import crud

router = APIRouter(tags=["Events"])


@router.get("/", response_model=Events)
async def get_events(
        date_from: datetime.date | None = None,
        date_to: datetime.date | None = None,
        doctor_id: int | None = None,
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):

    user = await authenticate(token, session)
    authorize(user, Role.DOCTOR)

    events = await crud.get_events(session=session, date_from=date_from, date_to=date_to, doctor_id=doctor_id)

    return events


@router.post("/")
async def post_event(
    event: ScheduleEvent,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = await authenticate(token, session)
    authorize(user, Role.DOCTOR)

    return await crud.create_or_update_event(event=event, session=session)
