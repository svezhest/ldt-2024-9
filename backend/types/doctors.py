import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber


class DoctorInfo(BaseModel):
    id: int
    full_name: str
    date_of_birth: datetime.date
    phone_number: PhoneNumber
    email: EmailStr
    position: str


class WorkStatus(Enum):
    WORKING = 1
    # работает
    BREAK = 2
    # зарезервируем такую возможность, но у них формат расписания слишком ограничен, чтобы так сделать
    HOME = 3
    # закончилось рабочее время
    VACATION = 4
    # в отпуске
    FORCE_MAJEURE = 5
    # форс мажор, не может работать


class DoctorWorkStatus(BaseModel):
    id: int
    status: WorkStatus


def parse_work_status(status: str):
    status = status.upper().strip()
    return WorkStatus[status]
