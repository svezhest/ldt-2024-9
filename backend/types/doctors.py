import datetime
from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from backend.types.schedule import WorkStatus


class DoctorInfo(BaseModel):
    id: int
    full_name: str
    date_of_birth: datetime.date
    phone_number: PhoneNumber
    email: EmailStr
    position: str


class DoctorWorkStatus(BaseModel):
    id: int
    status: WorkStatus
