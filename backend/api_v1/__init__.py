from fastapi import APIRouter

from .doctors.views import router as doctors_router
from .events.views import router as events_router

router = APIRouter()
router.include_router(router=doctors_router, prefix="/doctors")
router.include_router(router=events_router, prefix="/events")
