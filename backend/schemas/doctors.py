import datetime
from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from schemas.skills import Skills
from schemas.workload import WorkDayResults, WorkloadType
from schemas.schedule import WorkStatus


class DoctorInfo(BaseModel):
    id: int
    full_name: str
    date_of_birth: datetime.date
    phone_number: PhoneNumber
    email: EmailStr
    position: str
    skills: Skills


class DoctorWorkStatus(BaseModel):
    id: int
    status: WorkStatus


class DoctorDayResults(BaseModel):
    id: int
    results: WorkDayResults
