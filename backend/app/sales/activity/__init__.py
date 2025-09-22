from fastapi import APIRouter
from .activities import router as activities_router

router = APIRouter()
router.include_router(activities_router, prefix="/activities", tags=["activities"])