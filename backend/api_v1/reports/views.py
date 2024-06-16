import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.doctors.roles import Role
from api_v1.workload.workload import WorkloadType
from .schemas import Report
from auth import authenticate, oauth2_scheme
from authorize import authorize
from core.models import db_helper
from . import crud

router = APIRouter(tags=["Reports"])


@router.get("/{workload_type}/week", response_model=int)
async def get_total_for_this_week(
        workload_type: Annotated[WorkloadType, Path],
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):

    user = await authenticate(token, session)
    authorize(user, Role.DOCTOR)

    today = datetime.date.today()
    today += datetime.timedelta(days=-today.weekday())

    report = await crud.get_total_for_week(today, today + datetime.timedelta(days=6), workload_type, session)

    return report


@router.get("/{workload_type}/{doctor_id}", response_model=Report)
async def get_report(
        workload_type: Annotated[WorkloadType, Path],
        doctor_id: Annotated[int, Path],
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):

    user = await authenticate(token, session)
    authorize(user, Role.DOCTOR)

    report = await crud.get_report(doctor_id, datetime.date.today(), workload_type, session)

    return report


@router.post("/{workload_type}/{doctor_id}")
async def post_report(
        workload_type: Annotated[WorkloadType, Path],
        doctor_id: Annotated[int, Path],
        amount: int,
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):

    user = await authenticate(token, session)
    authorize(user, Role.DOCTOR)

    report = await crud.post_report(doctor_id, datetime.date.today(), workload_type, amount, session)

    return report
