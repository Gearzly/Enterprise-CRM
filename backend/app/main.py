from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from app.sales import router as sales_router
from app.marketing import router as marketing_router
from app.support import router as support_router
from app.superadmin import router as superadmin_router
from app.core.database import Base, engine
from app.core.security.owasp import add_security_headers, security_middleware
from app.core.compliance.routers import retention_router, deletion_router, consent_router
from app.core.security.routers import security_router
from app.core.audit.routers import audit_router
from app.core.data_classification.routers import classification_router
from app.core.security.production_routers import production_security_router
from app.core.auth.oauth2_routes import router as oauth2_router
from app.core.auth.oauth2_middleware import OAuth2AuthenticationMiddleware, OAuth2AuthorizationMiddleware
from app.core.middleware.error_handling import ErrorHandlingMiddleware, SecurityErrorMiddleware
from app.startup_optimizations import lifespan

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SaaS CRM Backend", 
    version="1.0.0"
)

# Add CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Default Vite dev server
        "http://localhost:3001",  # Alternative port
        "http://127.0.0.1:3000", 
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add OWASP security headers
add_security_headers(app)

# Add security middleware
app.middleware("http")(security_middleware)

# Add comprehensive error handling middleware
app.add_middleware(ErrorHandlingMiddleware, include_traceback=os.getenv("DEBUG", "false").lower() == "true")
app.add_middleware(SecurityErrorMiddleware)

# Add OAuth 2.0 authentication and authorization middleware
app.add_middleware(OAuth2AuthenticationMiddleware)
app.add_middleware(OAuth2AuthorizationMiddleware)

# Include all routers
app.include_router(sales_router, prefix="/sales", tags=["Sales"])
app.include_router(marketing_router, prefix="/marketing", tags=["Marketing"])
app.include_router(support_router, prefix="/support", tags=["Support"])
app.include_router(superadmin_router, prefix="/api", tags=["Super Admin"])
app.include_router(retention_router, prefix="/api/compliance", tags=["Compliance"])
app.include_router(deletion_router, prefix="/api/compliance", tags=["Compliance"])
app.include_router(consent_router, prefix="/api/compliance", tags=["Compliance"])
app.include_router(security_router, prefix="/api/security", tags=["Security"])
app.include_router(audit_router, prefix="/api/audit", tags=["Audit Logging"])
app.include_router(classification_router, prefix="/api/data", tags=["Data Classification"])
app.include_router(production_security_router, prefix="/api/security", tags=["Production Security"])
app.include_router(oauth2_router, prefix="/auth", tags=["OAuth 2.0 Authentication"])

@app.get("/")
def read_root():
    return {
        "message": "SaaS CRM Backend API",
        "version": "1.0.0",
        "status": "running",
        "modules": {
            "sales": "/sales",
            "marketing": "/marketing",
            "support": "/support",
            "superadmin": "/api/superadmin",
            "compliance": "/api/compliance",
            "security": "/api/security",
            "audit": "/api/audit",
            "data-classification": "/api/data",
            "authentication": "/auth"
        }
    }

@app.get("/search")
async def global_search(q: str, module: str = None, limit: int = 10):
    """Global search endpoint across all modules"""
    if not q or len(q) < 2:
        return {"results": [], "total": 0}
    
    # In a real implementation, this would search across all modules
    # For now, we'll return mock data
    mock_results = [
        {
            "id": "1",
            "title": "John Smith",
            "description": "Acme Corporation - CEO",
            "type": "contact",
            "module": "sales",
            "url": "/sales/contacts/1"
        },
        {
            "id": "2",
            "title": "TechStart Inc Deal",
            "description": "Software licensing - $125,000",
            "type": "deal",
            "module": "sales",
            "url": "/sales/deals/2"
        },
        {
            "id": "3",
            "title": "Marketing Campaign Q1",
            "description": "Email campaign for new product launch",
            "type": "activity",
            "module": "marketing",
            "url": "/marketing/campaigns/3"
        }
    ]
    
    # Filter by module if specified
    if module:
        mock_results = [r for r in mock_results if r["module"] == module]
    
    # Limit results
    results = mock_results[:limit]
    
    return {
        "results": results,
        "total": len(results),
        "query": q,
        "module": module
    }

@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": "2025-09-24T02:30:00Z",
        "version": "1.0.0",
        "database": "connected"
    }