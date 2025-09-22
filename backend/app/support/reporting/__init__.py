from fastapi import APIRouter
from .reporting import router as reporting_router

router = APIRouter()
router.include_router(reporting_router, prefix="/reporting", tags=["reporting"])