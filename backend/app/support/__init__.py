from fastapi import APIRouter
from .tickets import router as tickets_router
from .knowledge_base import router as knowledge_base_router
from .interactions import router as interactions_router
from .live_chat import router as live_chat_router
from .call_center import router as call_center_router
from .social_support import router as social_support_router
from .feedback import router as feedback_router
from .sla import router as sla_router
from .asset import router as asset_router
from .remote import router as remote_router
from .community import router as community_router
from .reporting import router as reporting_router
from .automation import router as automation_router
from .mobile import router as mobile_router
from .integration import router as integration_router
from .language import router as language_router

router = APIRouter()
router.include_router(tickets_router, prefix="/tickets", tags=["tickets"])
router.include_router(knowledge_base_router, prefix="/knowledge-base", tags=["knowledge-base"])
router.include_router(interactions_router, prefix="/interactions", tags=["interactions"])
router.include_router(live_chat_router, prefix="/live-chat", tags=["live-chat"])
router.include_router(call_center_router, prefix="/call-center", tags=["call-center"])
router.include_router(social_support_router, prefix="/social-support", tags=["social-support"])
router.include_router(feedback_router, prefix="/feedback", tags=["feedback"])
router.include_router(sla_router, prefix="/sla", tags=["sla"])
router.include_router(asset_router, prefix="/asset", tags=["asset"])
router.include_router(remote_router, prefix="/remote", tags=["remote"])
router.include_router(community_router, prefix="/community", tags=["community"])
router.include_router(reporting_router, prefix="/reporting", tags=["reporting"])
router.include_router(automation_router, prefix="/automation", tags=["automation"])
router.include_router(mobile_router, prefix="/mobile", tags=["mobile"])
router.include_router(integration_router, prefix="/integration", tags=["integration"])
router.include_router(language_router, prefix="/language", tags=["language"])

@router.get("/")
def get_support_dashboard():
    return {"message": "Support Dashboard"}