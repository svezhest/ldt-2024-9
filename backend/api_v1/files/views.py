import datetime
import time
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import FileResponse
import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.doctors.crud import get_doctors_confident
from api_v1.events.crud import get_events
from logic.generate_files import generate_doctor_table

from api_v1.doctors.roles import Role
from auth import authenticate, oauth2_scheme
from authorize import authorize
from core.models import db_helper

router = APIRouter(tags=["Files"])


@router.get("/predictions.xlsx")
async def download_predictions_in_xlsx(
    token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    user = await authenticate(token, session)
    authorize(user, Role.ADMIN)

    return FileResponse(path='predictions.xlsx', filename='predictions.xlsx', media_type='multipart/form-data')


@router.get("/predictions.csv")
async def download_predictions_in_csv(
    token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    user = await authenticate(token, session)
    authorize(user, Role.ADMIN)

    return FileResponse(path='predictions.csv', filename='predictions.csv', media_type='multipart/form-data')


@router.get("/table.xlsx")
async def download_table(
    date: datetime.date,
    token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    user = await authenticate(token, session)
    authorize(user, Role.ADMIN)

    doctors = await get_doctors_confident(session)

    start_date = date + datetime.timedelta(days=-date.day + 1)
    end_date = start_date + datetime.timedelta(days=31)

    events = await get_events(session=session, date_from=start_date, date_to=end_date)

    generate_doctor_table(doctors=doctors, date=start_date, events=events)

    return FileResponse(path='table.xlsx', filename='table.xlsx', media_type='multipart/form-data')
