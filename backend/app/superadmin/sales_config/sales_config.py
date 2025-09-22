from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime
from ..models import SalesConfig, SalesConfigCreate, SalesConfigUpdate

router = APIRouter()

# In-memory storage for demo purposes
sales_config_db = [
    SalesConfig(
        id=1,
        key="lead_statuses",
        value='["New", "Contacted", "Qualified", "Unqualified", "Converted"]',
        description="Available lead statuses",
        category="lead",
        organization_id=None,
        created_at=datetime.now()
    ),
    SalesConfig(
        id=2,
        key="lead_sources",
        value='["Website", "Referral", "Social Media", "Email Campaign", "Event", "Other"]',
        description="Available lead sources",
        category="lead",
        organization_id=None,
        created_at=datetime.now()
    ),
    SalesConfig(
        id=3,
        key="opportunity_stages",
        value='["Prospecting", "Qualification", "Proposal", "Negotiation", "Closed Won", "Closed Lost"]',
        description="Available opportunity stages",
        category="opportunity",
        organization_id=None,
        created_at=datetime.now()
    ),
    SalesConfig(
        id=4,
        key="quotation_statuses",
        value='["Draft", "Sent", "Viewed", "Accepted", "Rejected", "Expired"]',
        description="Available quotation statuses",
        category="quotation",
        organization_id=None,
        created_at=datetime.now()
    ),
    SalesConfig(
        id=5,
        key="default_tax_rate",
        value="0.0",
        description="Default tax rate for quotations",
        category="quotation",
        organization_id=None,
        created_at=datetime.now()
    ),
    SalesConfig(
        id=6,
        key="closed_won_stage",
        value="Closed Won",
        description="Stage name for closed won opportunities",
        category="reporting",
        organization_id=None,
        created_at=datetime.now()
    ),
    SalesConfig(
        id=7,
        key="forecast_factors",
        value='["Market growth", "New product launch", "Seasonal trends", "Economic conditions", "Competitor activity", "Historical trends"]',
        description="Available factors affecting sales forecasts",
        category="target",
        organization_id=None,
        created_at=datetime.now()
    ),
    SalesConfig(
        id=8,
        key="target_periods",
        value='["Q1", "Q2", "Q3", "Q4", "H1", "H2", "Annual", "Monthly"]',
        description="Available target periods",
        category="target",
        organization_id=None,
        created_at=datetime.now()
    )
]

@router.get("/", response_model=List[SalesConfig])
def list_sales_configs(category: Optional[str] = None, organization_id: Optional[int] = None):
    """List all sales configurations, optionally filtered by category or organization"""
    result = sales_config_db
    
    if category:
        result = [config for config in result if config.category == category]
    
    if organization_id is not None:
        # Include both global configs (organization_id=None) and org-specific configs
        result = [config for config in result if config.organization_id is None or config.organization_id == organization_id]
    
    return result

@router.get("/{config_id}", response_model=SalesConfig)
def get_sales_config(config_id: int):
    """Get a specific sales configuration by ID"""
    for config in sales_config_db:
        if config.id == config_id:
            return config
    raise HTTPException(status_code=404, detail="Sales configuration not found")

@router.post("/", response_model=SalesConfig)
def create_sales_config(config: SalesConfigCreate):
    """Create a new sales configuration"""
    new_id = max([c.id for c in sales_config_db]) + 1 if sales_config_db else 1
    new_config = SalesConfig(
        id=new_id,
        created_at=datetime.now(),
        **config.dict()
    )
    sales_config_db.append(new_config)
    return new_config

@router.put("/{config_id}", response_model=SalesConfig)
def update_sales_config(config_id: int, config_update: SalesConfigUpdate):
    """Update an existing sales configuration"""
    for index, config in enumerate(sales_config_db):
        if config.id == config_id:
            updated_config = SalesConfig(
                id=config_id,
                created_at=config.created_at,
                updated_at=datetime.now(),
                **config_update.dict()
            )
            sales_config_db[index] = updated_config
            return updated_config
    raise HTTPException(status_code=404, detail="Sales configuration not found")

@router.delete("/{config_id}")
def delete_sales_config(config_id: int):
    """Delete a sales configuration"""
    for index, config in enumerate(sales_config_db):
        if config.id == config_id:
            del sales_config_db[index]
            return {"message": "Sales configuration deleted successfully"}
    raise HTTPException(status_code=404, detail="Sales configuration not found")

@router.get("/key/{key}", response_model=SalesConfig)
def get_sales_config_by_key(key: str, organization_id: Optional[int] = None):
    """Get a sales configuration by key, with optional organization override"""
    # First check for organization-specific config
    if organization_id is not None:
        for config in sales_config_db:
            if config.key == key and config.organization_id == organization_id:
                return config
    
    # If no org-specific config found, return global config
    for config in sales_config_db:
        if config.key == key and config.organization_id is None:
            return config
    
    raise HTTPException(status_code=404, detail=f"Sales configuration with key '{key}' not found")

@router.get("/categories", response_model=List[str])
def list_categories():
    """List all sales configuration categories"""
    categories = list(set([config.category for config in sales_config_db]))
    return categories