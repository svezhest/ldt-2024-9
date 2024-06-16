import datetime
import time
from fastapi import APIRouter, HTTPException, status, Depends
import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.doctors.roles import Role
from api_v1.schedule.schemas import DaySchedule, Interval, Schedule, StartHours
from auth import authenticate, oauth2_scheme
from authorize import authorize
from core.models import db_helper
from . import crud
from .dependencies import doctor_by_id
from .schemas import Doctor, DoctorConfidentInfoReturn, DoctorPublicInfo, DoctorConfidentInfo, DoctorPartial, DoctorPublicInfoReturn, DoctorTechnicalInfo
from logic.calculate_schedule import calculate_schedule


router = APIRouter(tags=["Doctors"])


@router.get("/me", response_model=DoctorConfidentInfoReturn)
async def get_myself(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    user = await authenticate(token, session)
    user.skills = crud.deserialize_skills(user.skills)
    return user


@router.get("/", response_model=list[DoctorPublicInfoReturn])
async def get_doctors(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = await authenticate(token, session)
    authorize(user, [])
    return await crud.get_doctors(session=session)


@router.post(
    "/",
    response_model=DoctorConfidentInfoReturn,
    status_code=status.HTTP_201_CREATED,
)
async def create_doctor(
    doctor_in: DoctorTechnicalInfo,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = await authenticate(token, session)
    authorize(user, Role.HR)
    print(doctor_in)
    return await crud.create_doctor(session=session, doctor_in=doctor_in)


@router.get("/{doctor_id}/", response_model=DoctorConfidentInfoReturn)
async def get_doctor(
    doctor: Doctor = Depends(doctor_by_id),
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = await authenticate(token, session)
    authorize(user, Role.HR)
    return doctor


@router.patch("/{doctor_id}/")
async def update_doctor_partial(
    doctor_update: DoctorPartial,
    doctor: Doctor = Depends(doctor_by_id),
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = await authenticate(token, session)
    authorize(user, Role.HR)
    return await crud.update_doctor(
        session=session,
        doctor=doctor,
        doctor_update=doctor_update,
        partial=True,
    )


@router.patch("/{doctor_id}/password")
async def change_password(
    password: str,
    doctor: Doctor = Depends(doctor_by_id),
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = await authenticate(token, session)
    if doctor.id != user.id:
        authorize(user, Role.ADMIN)
    return await crud.change_password_doctor(
        session=session,
        doctor=doctor,
        password=password,
    )


@router.patch("/{doctor_id}/account_status")
async def change_account_status(
    account_status: str,
    doctor: Doctor = Depends(doctor_by_id),
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = await authenticate(token, session)
    authorize(user, Role.ADMIN)
    return await crud.change_account_status_doctor(
        session=session,
        doctor=doctor,
        account_status=account_status,
    )


@router.delete("/{doctor_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor(
    doctor: Doctor = Depends(doctor_by_id),
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    user = await authenticate(token, session)
    authorize(user, Role.ADMIN)
    await crud.delete_doctor(session=session, doctor=doctor)


@router.get("/{doctor_id}/schedule", response_model=Schedule)
async def get_schedule(
    date_from: datetime.date,
    date_to: datetime.date,
    doctor: Doctor = Depends(doctor_by_id),
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = await authenticate(token, session)
    authorize(user, [Role.DOCTOR, Role.HR])

    return calculate_schedule(date_from=date_from, date_to=date_to, doctor=doctor)
