from fastapi import APIRouter
from .quotations import router as quotations_router

router = APIRouter()
router.include_router(quotations_router, prefix="/quotations", tags=["quotations"])