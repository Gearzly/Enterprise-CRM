from fastapi import APIRouter
from .community import router as community_router

router = APIRouter()
router.include_router(community_router, prefix="/community", tags=["community"])