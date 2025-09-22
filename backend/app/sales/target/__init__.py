from fastapi import APIRouter
from .targets import router as targets_router

router = APIRouter()
router.include_router(targets_router, prefix="/targets", tags=["targets"])