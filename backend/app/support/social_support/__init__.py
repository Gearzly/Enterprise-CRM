from fastapi import APIRouter
from .social_support import router as social_support_router

router = APIRouter()
router.include_router(social_support_router, prefix="/social-support", tags=["social-support"])