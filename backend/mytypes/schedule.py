
import datetime
from enum import Enum
from pydantic import BaseModel


class WorkStatus(Enum):
    WORKING = 1
    # работает
    BREAK = 2
    # отдых
    HOME = 3
    # закончилось рабочее время
    VACATION = 4
    # в отпуске
    FORCE_MAJEURE = 5
    # форс мажор, не может работать


def parse_work_status(status: str):
    status = status.upper().strip()
    return WorkStatus[status]


class Interval(BaseModel):
    '''
    Примеры:

    Работник в отпуске:
    {
        start_time: 00:00:01
        end_time: 23:59:59
        status: VACATION
    },

    Обычный рабочий день:
    {
        start_time: 08:00:00
        end_time: 13:30:00
        status: WORKING
    },

    {
        start_time: 13:30:00
        end_time: 14:00:00
        status: BREAK
    },

    {
        start_time: 14:00:00
        end_time: 17:30:00
        status: WORKING
    },

    '''
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
