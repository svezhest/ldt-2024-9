from fastapi import APIRouter, HTTPException, status, Depends
import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from auth import authenticate, oauth2_scheme
from core.models import db_helper
from . import crud
from .dependencies import doctor_by_id
from .schemas import Doctor, DoctorCreate, DoctorUpdate, DoctorUpdatePartial

router = APIRouter(tags=["Doctors"])


@router.get("/me")
async def get_myself(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    user = await authenticate(token, session)
    return user


@router.get("/", response_model=list[Doctor])
async def get_doctors(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = await authenticate(token, session)
    return await crud.get_doctors(session=session)


@router.post(
    "/",
    response_model=Doctor,
    status_code=status.HTTP_201_CREATED,
)
async def create_doctor(
    doctor_in: DoctorCreate,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = await authenticate(token, session)
    return await crud.create_doctor(session=session, doctor_in=doctor_in)


@router.get("/{doctor_id}/", response_model=Doctor)
async def get_doctor(
    doctor: Doctor = Depends(doctor_by_id),
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = await authenticate(token, session)
    return doctor


@router.put("/{doctor_id}/")
async def update_doctor(
    doctor_update: DoctorUpdate,
    doctor: Doctor = Depends(doctor_by_id),
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = await authenticate(token, session)
    return await crud.update_doctor(
        session=session,
        doctor=doctor,
        doctor_update=doctor_update,
    )


@router.patch("/{doctor_id}/")
async def update_doctor_partial(
    doctor_update: DoctorUpdatePartial,
    doctor: Doctor = Depends(doctor_by_id),
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = await authenticate(token, session)
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
    return await crud.change_password_doctor(
        session=session,
        doctor=doctor,
        password=password,
    )


@router.delete("/{doctor_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor(
    doctor: Doctor = Depends(doctor_by_id),
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    user = await authenticate(token, session)
    await crud.delete_doctor(session=session, doctor=doctor)
