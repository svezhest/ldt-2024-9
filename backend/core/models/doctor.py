import datetime
from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic import BaseModel, ConfigDict, EmailStr
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Doctor(Base):
    full_name: Mapped[str]
    date_of_birth: Mapped[datetime.date]
    phone_number: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    position: Mapped[str]
    specialization: Mapped[str]
    skills: Mapped[str]  # побьем сроку по ', '
    hashed_password: Mapped[str]
    role: Mapped[str]
    account_status: Mapped[str]
    start_hours: Mapped[str]
    shifting_type: Mapped[str]
    hours_per_week: Mapped[int]
