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


@router.get("/{doctor_id}/", response_model=Doctor)
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


def is_weekend(day: datetime.date):
    # TODO: production calendar
    return day.weekday() > 4


def add_hours(start: datetime.time, hours_delta: float) -> datetime.time:
    return (datetime.datetime.combine(datetime.date(
        1, 1, 1), start) + datetime.timedelta(hours=hours_delta)).time()


def generate_schedule(starting_hours: StartHours, duration: int):
    if duration >= 11:
        break_time = 1.
    else:
        break_time = 0.5

    first_half = duration // 2

    if starting_hours == '08:00':
        starting_hours = datetime.time(hour=8)
    elif starting_hours == '09:00':
        starting_hours = datetime.time(hour=9)
    elif starting_hours == '14:00':
        starting_hours = datetime.time(hour=14)
    elif starting_hours == '20:00':
        starting_hours = datetime.time(hour=20)

    return DaySchedule(
        intervals=[
            Interval(
                start_time=starting_hours,
                end_time=add_hours(starting_hours, first_half),
                is_break=False
            ),
            Interval(
                start_time=add_hours(starting_hours, first_half),
                end_time=add_hours(starting_hours, first_half + break_time),
                is_break=True
            ),
            Interval(
                start_time=add_hours(starting_hours, first_half + break_time),
                end_time=add_hours(starting_hours, duration + break_time),
                is_break=False
            ),
        ],
        date=datetime.date.today(),
        total_working_time=duration,
        total_break_time=break_time
    )


@router.get("/{doctor_id}/schedule", response_model=Schedule)
async def get_schedule(
    date_from: datetime.date,
    date_to: datetime.date,
    doctor: Doctor = Depends(doctor_by_id),
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    # 12 * 6 = 72, 12 * 7 = 84
    # 11 * 4 + 12 * 3 = 44 + 36 = 80
    # 2/2 (80, 2w): 01 02 03 04 05 06 07 08 09 10 11 12 13 14
    #               11 -- 12 11 -- -- 12 -- 11 -- -- 12 11 --

    # 12 * 5 = 60
    # 2/2 (60, 2w): 01 02 03 04 05 06 07 08 09 10 11 12 13 14
    #               12 -- -- 12 -- -- 12 -- 12 -- -- 12 -- --

    # 12 * 3 = 36, 12 * 4 = 48 -- тут не получится
    # 2/2 (80, 4w): 01 02 03 04 05 06 07 08 09 10 11 12 13 14 01 02 03 04 05 06 07 08 09 10 11 12 13 14
    #               -- 11 -- -- -- 12 -- -- 11 -- -- -- -- 12 -- -- -- 11 -- -- -- 12 -- -- -- 11 -- --

    user = await authenticate(token, session)
    authorize(user, [Role.DOCTOR, Role.HR])

    res = []

    if doctor.shifting_type == '5/2':
        if doctor.hours_per_week == 20:
            current_date = date_from + \
                datetime.timedelta(days=-date_from.weekday())
            while current_date <= date_to:
                if not is_weekend(current_date) and current_date >= date_from and current_date.weekday() < 3:
                    day_schedule = generate_schedule(doctor.start_hours,
                                                     7 if current_date.weekday() < 2 else 6)
                    day_schedule.date = current_date
                    res.append(day_schedule)
                current_date += datetime.timedelta(days=1)
        else:
            current_date = date_from
            while current_date <= date_to:
                if not is_weekend(current_date):
                    day_schedule = generate_schedule(doctor.start_hours,
                                                     6 if doctor.hours_per_week == 30 else 8)
                    day_schedule.date = current_date
                    res.append(day_schedule)
                current_date += datetime.timedelta(days=1)
    else:
        first_month_day = date_from + datetime.timedelta(days=-date_from.day)
        current_date = first_month_day + \
            datetime.timedelta(days=-first_month_day.weekday)

        if doctor.hours_per_week == 20:
            schedule_4_weeks = [
                0, 11, 0, 0, 0, 12, 0, 0, 11, 0, 0, 0, 0, 12, 0, 0, 0, 11, 0, 0, 0, 12, 0, 0, 0, 11, 0, 0
            ]
        elif doctor.hours_per_week == 30:
            schedule_4_weeks = [
                12, 0, 0, 12, 0, 0, 12, 0, 12, 0, 0, 12, 0, 0, 12, 0, 0, 12, 0, 0, 12, 0, 12, 0, 0, 12, 0, 0
            ]
        elif doctor.hours_per_week == 40:
            schedule_4_weeks = [
                11, 0, 12, 11, 0, 0, 12, 0, 11, 0, 0, 12, 11, 0, 11, 0, 12, 11, 0, 0, 12, 0, 11, 0, 0, 12, 11, 0
            ]

        idx = 0
        while current_date <= date_to:
            if current_date >= date_from:
                if schedule_4_weeks[idx] == 0:
                    day_schedule = DaySchedule(
                        intervals=[],
                        date=current_date,
                        total_break_time=0,
                        total_working_time=0
                    )
                else:
                    day_schedule = generate_schedule(
                        doctor.start_hours,
                        schedule_4_weeks[idx])
                    day_schedule.date = current_date
                res.append(day_schedule)
            current_date += datetime.timedelta(days=1)
            idx = (idx + 1) % 28

    return Schedule(
        schedule=res
    )
