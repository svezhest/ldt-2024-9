import datetime
from pydantic import BaseModel, ConfigDict, field_serializer
from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from api_v1.doctors.roles import AccountStatus, Role
from api_v1.doctors.skills import Skills


# class DoctorBase(BaseModel):
#     full_name: str
#     date_of_birth: datetime.date
#     phone_number: PhoneNumber
#     email: EmailStr
#     position: str
#     specialization: str
#     skills: Skills
#     password: str
#     role: Role
#     account_status: AccountStatus = AccountStatus.UNKOWN

class DoctorPublicInfo(BaseModel):
    full_name: str
    date_of_birth: datetime.date
    position: str
    specialization: str


class DoctorConfidentInfo(DoctorPublicInfo):
    phone_number: PhoneNumber
    email: EmailStr
    skills: Skills
    role: Role


class DoctorTechnicalInfo(DoctorConfidentInfo):
    password: str
    account_status: AccountStatus = AccountStatus.NEW


class DoctorPartial(DoctorTechnicalInfo):
    full_name: str | None = None
    date_of_birth: datetime.date | None = None
    phone_number: PhoneNumber | None = None
    email: EmailStr | None = None
    position: str | None = None
    specialization: str | None = None
    skills: Skills | None = None
    role: Role | None = None


class Doctor(DoctorTechnicalInfo):
    model_config = ConfigDict(from_attributes=True)
    id: int
