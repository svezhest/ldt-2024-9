from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud
from .dependencies import doctor_by_id
from .schemas import Doctor, DoctorCreate, DoctorUpdate, DoctorUpdatePartial

router = APIRouter(tags=["Doctors"])


@router.get("/", response_model=list[Doctor])
async def get_doctors(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_doctors(session=session)


@router.post(
    "/",
    response_model=Doctor,
    status_code=status.HTTP_201_CREATED,
)
async def create_doctor(
    doctor_in: DoctorCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_doctor(session=session, doctor_in=doctor_in)


@router.get("/{doctor_id}/", response_model=Doctor)
async def get_doctor(
    doctor: Doctor = Depends(doctor_by_id),
):
    return doctor


@router.put("/{doctor_id}/")
async def update_doctor(
    doctor_update: DoctorUpdate,
    doctor: Doctor = Depends(doctor_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_doctor(
        session=session,
        doctor=doctor,
        doctor_update=doctor_update,
    )


@router.patch("/{doctor_id}/")
async def update_doctor_partial(
    doctor_update: DoctorUpdatePartial,
    doctor: Doctor = Depends(doctor_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_doctor(
        session=session,
        doctor=doctor,
        doctor_update=doctor_update,
        partial=True,
    )


@router.delete("/{doctor_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor(
    doctor: Doctor = Depends(doctor_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_doctor(session=session, doctor=doctor)
