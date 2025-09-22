from fastapi import APIRouter
from .activity import router as activity_router
from .contact import router as contact_router
from .lead import router as lead_router
from .opportunity import router as opportunity_router
from .quotation import router as quotation_router
from .report import router as report_router
from .target import router as target_router

router = APIRouter()
router.include_router(activity_router, prefix="/activity", tags=["activity"])
router.include_router(contact_router, prefix="/contact", tags=["contact"])
router.include_router(lead_router, prefix="/lead", tags=["lead"])
router.include_router(opportunity_router, prefix="/opportunity", tags=["opportunity"])
router.include_router(quotation_router, prefix="/quotation", tags=["quotation"])
router.include_router(report_router, prefix="/report", tags=["report"])
router.include_router(target_router, prefix="/target", tags=["target"])

@router.get("/")
def get_sales_dashboard():
    return {
        "message": "Sales Dashboard",
        "modules": [
            "activities",
            "contacts",
            "leads",
            "opportunities",
            "quotations",
            "reports",
            "targets"
        ]
    }