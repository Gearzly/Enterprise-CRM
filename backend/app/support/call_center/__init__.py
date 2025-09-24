from fastapi import APIRouter
from .call_center import router as call_center_router

router = call_center_router