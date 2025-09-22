from fastapi import APIRouter
from .content import router as content_router

router = APIRouter()
router.include_router(content_router, prefix="/content", tags=["content"])