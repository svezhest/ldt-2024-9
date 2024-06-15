from sqlalchemy import Column, Integer, String, Enum, Time, Date, Interval as SQLAlchemyInterval, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum
import datetime

from api_v1.schedule.schemas import WorkStatus

Base = declarative_base()

class Interval(Base):
    __tablename__ = 'intervals'
    
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    status = Column(Enum(WorkStatus), nullable=False)
    id = Column(Integer, primary_key=True, index=True)

class DaySchedule(Base):
    __tablename__ = 'day_schedules'
    
    day_in_month = Column(Integer, primary_key=True, nullable=False)
    total_break_time = Column(SQLAlchemyInterval, nullable=False)
    total_working_time = Column(SQLAlchemyInterval, nullable=False)
    schedule_id = Column(Integer, ForeignKey('schedules.id'), primary_key=True)
    
    intervals = relationship("Interval", back_populates="day_schedule")

class Schedule(Base):
    __tablename__ = 'schedules'
    
    id = Column(Integer, primary_key=True, index=True)
    
    day_schedules = relationship("DaySchedule", back_populates="schedule")

Interval.day_schedule = relationship("DaySchedule", back_populates="intervals")
DaySchedule.schedule = relationship("Schedule", back_populates="day_schedules")
