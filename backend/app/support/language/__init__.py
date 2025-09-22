from fastapi import APIRouter
from .language import router as language_router

router = APIRouter()
router.include_router(language_router, prefix="/language", tags=["language"])