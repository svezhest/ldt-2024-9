from fastapi import APIRouter

from .doctors.views import router as doctors_router

router = APIRouter()
router.include_router(router=doctors_router, prefix="/doctors")
