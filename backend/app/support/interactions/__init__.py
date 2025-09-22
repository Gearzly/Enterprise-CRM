from fastapi import APIRouter
from .interactions import router as interactions_router

router = APIRouter()
router.include_router(interactions_router, prefix="/interactions", tags=["interactions"])