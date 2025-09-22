from fastapi import APIRouter
from .mobile import router as mobile_router

router = APIRouter()
router.include_router(mobile_router, prefix="/mobile", tags=["mobile"])