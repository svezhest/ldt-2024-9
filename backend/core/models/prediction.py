import datetime
from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic import BaseModel, ConfigDict, EmailStr
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

from core.models.base import Base


class Prediction(Base):
    date: Mapped[datetime.date] = mapped_column(primary_key=True)
    workload_type: Mapped[str] = mapped_column(primary_key=True)
    amount: Mapped[int]
