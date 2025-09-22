from fastapi import APIRouter
from .cdp import router as cdp_router

router = APIRouter()
router.include_router(cdp_router, prefix="/cdp", tags=["cdp"])