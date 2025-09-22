from fastapi import APIRouter
from .call_center import router as call_center_router

router = APIRouter()
router.include_router(call_center_router, prefix="/call-center", tags=["call-center"])