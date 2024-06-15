"""
Create
Read
Update
Delete
"""

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from api_v1.doctors.roles import AccountStatus
from api_v1.doctors.skills import Skills
from core.models import Doctor

from .schemas import DoctorPublicInfo, DoctorConfidentInfo, DoctorPartial, DoctorTechnicalInfo
from .schemas import Doctor as DoctorRepr
from auth import get_password_hash

async def get_doctors(session: AsyncSession) -> list[DoctorPublicInfo]:
    stmt = select(Doctor).order_by(Doctor.id)
    result: Result = await session.execute(stmt)
    doctors = result.scalars().all()

    for doctor in doctors:
        doctor.skills = deserialize_skills(doctor.skills)

    return list(doctors)


async def get_doctor(session: AsyncSession, doctor_id: int) -> DoctorRepr | None:
    doctor = await session.get(Doctor, doctor_id)
    doctor.skills = deserialize_skills(doctor.skills)
    return doctor


def serialize_skills(skills: Skills) -> str:
    return ', '.join([skills.primary_skill, *skills.secondary_skills])


def deserialize_skills(skills: str) -> Skills:
    return Skills(primary_skill=skills.split(', ')[0], secondary_skills=skills.split(', ')[1:])


async def create_doctor(session: AsyncSession, doctor_in: DoctorRepr) -> Doctor:
    doctor = Doctor(**doctor_in.model_dump(exclude=['skills', 'password', 'account_status']),
                    skills=serialize_skills(doctor_in.skills),
                    hashed_password=get_password_hash(doctor_in.password),
                    account_status='new')
    session.add(doctor)
    await session.commit()
    # await session.refresh(doctor)
    doctor.skills = deserialize_skills(doctor.skills)
    return doctor


async def update_doctor(
    session: AsyncSession,
    doctor: Doctor,
    doctor_update: DoctorPartial,
) -> Doctor:
    for name, value in doctor_update.model_dump(exclude_unset=True).items():
        setattr(doctor, name, value)
    doctor.skills = serialize_skills(doctor.skills)
    doctor.account_status = AccountStatus.NEW
    await session.commit()
    doctor.skills = deserialize_skills(doctor.skills)
    return doctor

async def change_password_doctor(
    session: AsyncSession,
    doctor: Doctor,
    password: str
) -> Doctor:
    doctor.hashed_password = get_password_hash(password)
    doctor.skills = serialize_skills(doctor.skills)
    await session.commit()
    doctor.skills = deserialize_skills(doctor.skills)
    return doctor

async def change_account_status_doctor(
    session: AsyncSession,
    doctor: Doctor,
    account_status: AccountStatus
) -> Doctor:
    doctor.account_status = account_status
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
