from fastapi import APIRouter
from .organizations import router as org_router
from .security import router as security_router
from .settings import router as settings_router
from .modules import router as modules_router
from .sales_config import router as sales_config_router
from .marketing_config import router as marketing_config_router
from .support_config import router as support_config_router

router = APIRouter(prefix="/superadmin", tags=["Super Admin"])

# Include all sub-routers
router.include_router(org_router)
router.include_router(security_router)
router.include_router(settings_router)
router.include_router(modules_router)
router.include_router(sales_config_router)
router.include_router(marketing_config_router)
router.include_router(support_config_router)

@router.get("/")
def get_superadmin_dashboard():
    return {
        "message": "Super Admin Dashboard",
        "modules": [
            "organizations",
            "security",
            "settings",
            "modules",
            "sales-config",
            "marketing-config",
            "support-config"
        ]
    }