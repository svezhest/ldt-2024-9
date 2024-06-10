
import datetime
from pydantic import BaseModel

from backend.types.doctors import WorkStatus


class Interval(BaseModel):
    start_time: datetime.time
    end_time: datetime.time
    status: WorkStatus


class DaySchedule(BaseModel):
    intervals: list[Interval]
    date: datetime.date
    total_break_time: datetime.timedelta
    total_working_time: datetime.timedelta


class Schedule(BaseModel):
    doctor_id: int
    schedule: list[DaySchedule]
