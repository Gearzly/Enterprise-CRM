from fastapi import APIRouter
from .partners import router as partners_router

router = APIRouter()
router.include_router(partners_router, prefix="/partners", tags=["partners"])