from fastapi import APIRouter
from .opportunities import router as opportunities_router

router = APIRouter()
router.include_router(opportunities_router, prefix="/opportunities", tags=["opportunities"])