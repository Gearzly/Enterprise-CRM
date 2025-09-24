from fastapi import APIRouter
from .sla import router as sla_router

router = sla_router