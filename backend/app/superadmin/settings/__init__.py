from fastapi import APIRouter
from .settings import router as settings_router

router = APIRouter(prefix="/settings", tags=["System Settings"])
router.include_router(settings_router)