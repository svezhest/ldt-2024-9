# import datetime
# from fastapi import APIRouter, HTTPException, status, Depends
# import jwt
# from sqlalchemy.ext.asyncio import AsyncSession

# from api_v1.doctors.roles import Role
# from auth import authenticate, oauth2_scheme
# from authorize import authorize
# from core.models import db_helper
# from . import crud
# router = APIRouter(tags=["Schedule"])

# # DAY SCHEDULE

# @router.get("/day_schedules/")

# @router.get("/day_schedules/{day_schedule_id}")

# @router.post("/day_schedules/")

# # 

#     {
#         doctor_id: number,
#         day: date,
#         work_start: "08:00",
#         work_end: "20:00",
#     }


# @router.get("/{schedule_id}")
# async def get_schedule(
#         from_date: datetime.date,
#         to_date: datetime.date,
#         token: str = Depends(oauth2_scheme),
#         session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
#     '''
#     Returns work schedule for each day in interval (including to_date).
#     Does not include vacation, paid leaves, unpaid leaves, etc.
#     '''
    
#     user = await authenticate(token, session)
#     authorize(user, [Role.DOCTOR, Role.HR])

#     user.skills = crud.deserialize_skills(user.skills)
#     return user


