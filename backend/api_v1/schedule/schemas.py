
import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict


# class WorkStatus(str, Enum):
#     WORKING = 'working'
#     # работает
#     BREAK = 'break'
#     # отдых
#     HOME = 'home'
#     # закончилось рабочее время
#     VACATION = 'vacation'
#     # в отпуске
#     FORCE_MAJEURE = 'force_majeure'
#     # форс мажор, не может работать


# def parse_work_status(status: str):
#     status = status.upper().strip()
#     return WorkStatus[status]


# class Interval(BaseModel):
#     '''
#     Примеры:

#     Работник в отпуске:
#     {
#         start_time: 00:00:01
#         end_time: 23:59:59
#         status: VACATION
#     },

#     Обычный рабочий день:
#     {
#         start_time: 08:00:00
#         end_time: 13:30:00
#         status: WORKING
#     },

#     {
#         start_time: 13:30:00
#         end_time: 14:00:00
#         status: BREAK
#     },

#     {
#         start_time: 14:00:00
#         end_time: 17:30:00
#         status: WORKING
#     },

#     '''
#     start_time: datetime.time
#     end_time: datetime.time
#     status: WorkStatus


# class DaySchedule(BaseModel):
#     intervals: list[Interval]
#     date: datetime.date
#     total_break_time: datetime.timedelta
#     total_working_time: datetime.timedelta


# class Schedule(BaseModel):
#     doctor_id: int
#     schedule: list[DaySchedule]

class WorkStatus(str, Enum):
    WORKING = 'working' 
    HOME = 'home'
    VACATION = 'vacation'
    FORCE_MAJEURE = 'force_majeure'
    OVERTIME = 'overtime'

class ShiftingType(str, Enum):
    FIVE_TWO = '5/2'
    TWO_TWO = '2/2'

class StartHours(str, Enum):
    EIGHT = '08:00'
    NINE = '09:00'
    TWO_PM = '14:00'
    EIGHT_PM = '20:00'

class HoursPerWeek(Enum):
    TWENTY = 20
    THIRTY = 30
    FOURTY = 40

class ScheduleMixin(BaseModel):
    start_hours: StartHours
    shifting_type: ShiftingType
    hours_per_weel: HoursPerWeek

class ScheduleEvent(BaseModel):
    doctor_id: int
    date: datetime.date
    work_status: WorkStatus