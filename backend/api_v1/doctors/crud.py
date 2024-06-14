"""
Create
Read
Update
Delete
"""

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from api_v1.doctors.skills import Skills
from core.models import Doctor

from .schemas import DoctorCreate, DoctorUpdate, DoctorUpdatePartial


async def get_doctors(session: AsyncSession) -> list[Doctor]:
    stmt = select(Doctor).order_by(Doctor.id)
    result: Result = await session.execute(stmt)
    doctors = result.scalars().all()

    for doctor in doctors:
        doctor.skills = deserialize_skills(doctor.skills)

    return list(doctors)


async def get_doctor(session: AsyncSession, doctor_id: int) -> Doctor | None:
    doctor = await session.get(Doctor, doctor_id)
    doctor.skills = deserialize_skills(doctor.skills)
    return doctor


def serialize_skills(skills: Skills) -> str:
    return ', '.join([skills.primary_skill, *skills.secondary_skills])


def deserialize_skills(skills: str) -> Skills:
    return Skills(primary_skill=skills.split(', ')[0], secondary_skills=skills.split(', ')[1:])


async def create_doctor(session: AsyncSession, doctor_in: DoctorCreate) -> Doctor:
    doctor = Doctor(**doctor_in.model_dump(exclude='skills'),
                    skills=serialize_skills(doctor_in.skills))
    session.add(doctor)
    await session.commit()
    # await session.refresh(doctor)
    doctor.skills = deserialize_skills(doctor.skills)
    return doctor


async def update_doctor(
    session: AsyncSession,
    doctor: Doctor,
    doctor_update: DoctorUpdate | DoctorUpdatePartial,
    partial: bool = False,
) -> Doctor:
    for name, value in doctor_update.model_dump(exclude_unset=partial).items():
        setattr(doctor, name, value)
    doctor.skills = serialize_skills(doctor.skills)
    await session.commit()
    doctor.skills = deserialize_skills(doctor.skills)
    return doctor


async def delete_doctor(
    session: AsyncSession,
    doctor: Doctor,
) -> None:
    await session.delete(doctor)
    await session.commit()
