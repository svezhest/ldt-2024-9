import datetime
from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic import BaseModel, ConfigDict, EmailStr
from sqlalchemy.orm import Mapped

from .base import Base


class Doctor(Base):
    full_name: Mapped[str]
    date_of_birth: Mapped[datetime.date]
    phone_number: Mapped[str]
    email: Mapped[str]
    position: Mapped[str]
    specialization: Mapped[str]
    skills: Mapped[str] # побьем сроку по ', '
