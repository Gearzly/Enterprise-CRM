from fastapi import FastAPI
from app.sales import router as sales_router
from app.marketing import router as marketing_router
from app.support import router as support_router
from app.superadmin import router as superadmin_router
from app.core.database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SaaS CRM Backend", version="1.0.0")

app.include_router(sales_router, prefix="/sales", tags=["Sales"])
app.include_router(marketing_router, prefix="/marketing", tags=["Marketing"])
app.include_router(support_router, prefix="/support", tags=["Support"])
app.include_router(superadmin_router, prefix="/api", tags=["Super Admin"])

@app.get("/")
def read_root():
    return {
        "message": "SaaS CRM Backend API",
        "version": "1.0.0",
        "modules": {
            "sales": "/sales",
            "marketing": "/marketing",
            "support": "/support",
            "superadmin": "/api/superadmin"
        }
    }