from fastapi import APIRouter
from .automation import router as automation_router

router = APIRouter()
router.include_router(automation_router, prefix="/automation", tags=["automation"])