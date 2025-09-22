from fastapi import APIRouter
from .social_media import router as social_media_router

router = APIRouter()
router.include_router(social_media_router, prefix="/social-media", tags=["social-media"])