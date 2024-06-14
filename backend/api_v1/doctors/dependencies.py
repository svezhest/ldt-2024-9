from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Doctor

from . import crud


async def doctor_by_id(
    doctor_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Doctor:
    doctor = await crud.get_doctor(session=session, doctor_id=doctor_id)
    if doctor is not None:
        return doctor

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Doctor {doctor_id} not found!",
    )
