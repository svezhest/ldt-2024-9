import datetime
from pydantic import BaseModel, ConfigDict, field_serializer
from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from api_v1.doctors.skills import Skills


class DoctorBase(BaseModel):
    full_name: str
    date_of_birth: datetime.date
    phone_number: PhoneNumber
    email: EmailStr
    position: str
    skills: Skills


class DoctorCreate(DoctorBase):
    pass


class DoctorUpdate(DoctorCreate):
    pass


class DoctorUpdatePartial(DoctorCreate):
    full_name: str | None = None
    date_of_birth: datetime.date | None = None
    phone_number: PhoneNumber | None = None
    email: EmailStr | None = None
    position: str | None = None
    skills: Skills | None = None


class Doctor(DoctorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
