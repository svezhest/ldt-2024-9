import datetime
from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic import BaseModel, ConfigDict, EmailStr
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'

    doctor_id: Mapped[int] = mapped_column(ForeignKey('doctors.id'), primary_key=True)
    date: Mapped[datetime.date] = mapped_column(primary_key=True, index=True)
    event_type: Mapped[str]
