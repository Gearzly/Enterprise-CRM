from fastapi import APIRouter
from .campaigns import router as campaigns_router
from .leads import router as leads_router
from .email import router as email_router
from .social_media import router as social_media_router
from .content import router as content_router
from .analytics import router as analytics_router
from .automation import router as automation_router
from .segmentation import router as segmentation_router
from .events import router as events_router
from .partners import router as partners_router
from .resources import router as resources_router
from .cdp import router as cdp_router

router = APIRouter()
router.include_router(campaigns_router, prefix="/campaigns", tags=["campaigns"])
router.include_router(leads_router, prefix="/leads", tags=["leads"])
router.include_router(email_router, prefix="/email", tags=["email"])
router.include_router(social_media_router, prefix="/social-media", tags=["social-media"])
router.include_router(content_router, prefix="/content", tags=["content"])
router.include_router(analytics_router, prefix="/analytics", tags=["analytics"])
router.include_router(automation_router, prefix="/automation", tags=["automation"])
router.include_router(segmentation_router, prefix="/segmentation", tags=["segmentation"])
router.include_router(events_router, prefix="/events", tags=["events"])
router.include_router(partners_router, prefix="/partners", tags=["partners"])
router.include_router(resources_router, prefix="/resources", tags=["resources"])
router.include_router(cdp_router, prefix="/cdp", tags=["cdp"])

@router.get("/")
def get_marketing_dashboard():
    return {"message": "Marketing Dashboard"}