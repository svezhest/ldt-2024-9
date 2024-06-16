"""
Create
Read
Update
Delete
"""

import datetime
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from api_v1.doctors.roles import AccountStatus
from api_v1.schedule.schemas import Events, ScheduleEvent
from core.models import Event

from typing import Union


async def get_events(
        session:  AsyncSession,
        date_from: datetime.date | None = None,
        date_to: datetime.date | None = None,
        doctor_id: int | None = None) -> Events:
    stmt = select(Event)

    if doctor_id is not None:
        stmt = stmt.where(Event.doctor_id == doctor_id)

    if date_from is not None:
        stmt = stmt.where(Event.date >= date_from)

    if date_to is not None:
        stmt = stmt.where(Event.date <= date_to)

    result: Result = await session.execute(stmt)

    events = [ScheduleEvent(doctor_id=event.doctor_id, date=event.date,
                            event_type=event.event_type) for event in result.scalars().all()]

    return Events(events=events)


async def create_or_update_event(
        session:  AsyncSession,
        event: ScheduleEvent,
):
    _event = await session.get(Event, (event.doctor_id, event.date))

    if _event is None:
        session.add(Event(doctor_id=event.doctor_id,
                    date=event.date, event_type=event.event_type))
    else:
        _event.event_type = event.event_type

    await session.commit()

    return _event
