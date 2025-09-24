from fastapi import APIRouter
from .cdp import router as cdp_router

router = cdp_router