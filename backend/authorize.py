from fastapi import HTTPException, status
from api_v1.doctors.roles import AccountStatus, Role
from core.models.doctor import Doctor


def authorize(doctor: Doctor, required_role: Role | list[Role]):
    role: Role = doctor.role
    id: int = doctor.id
    account_status: AccountStatus = doctor.account_status
    if type(required_role) is not list:
        required_role = [required_role]

    if not (account_status == AccountStatus.OK
            and (role == Role.ADMIN
                 or role in required_role or len(required_role) == 0)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insuffisient role",
            headers={"WWW-Authenticate": "Bearer"},
        )
