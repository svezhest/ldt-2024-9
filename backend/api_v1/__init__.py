from fastapi import APIRouter

from .doctors.views import router as doctors_router
from .events.views import router as events_router
from .reports.views import router as reports_router
from .stats.views import router as stats_router
from .files.views import router as files_router


router = APIRouter()
router.include_router(router=doctors_router, prefix="/doctors")
router.include_router(router=events_router, prefix="/events")
router.include_router(router=reports_router, prefix="/reports")
router.include_router(router=stats_router, prefix="/stats")
router.include_router(router=files_router, prefix="/files")
