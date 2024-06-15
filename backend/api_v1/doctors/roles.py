from enum import Enum

class Role(str, Enum):
    ADMIN = 'admin'
    HR = 'hr'
    ANALYST = 'analyst'
    DOCTOR = 'doctor'

class AccountStatus(str, Enum):
    NEW = 'new'
    OK = 'ok'
    DELETED = 'deleted'
