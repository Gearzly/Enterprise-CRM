from fastapi import APIRouter
from .segmentation import router as segmentation_router

router = APIRouter()
router.include_router(segmentation_router, prefix="/segmentation", tags=["segmentation"])