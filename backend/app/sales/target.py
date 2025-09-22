from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import httpx
import json

from .config import get_sales_config

router = APIRouter()

class SalesTargetBase(BaseModel):
    name: str
    period: str  # e.g., "Q1 2025", "2025", "January 2025"
    target_amount: float
    assigned_to: Optional[str] = None
    description: Optional[str] = None

class SalesTargetCreate(SalesTargetBase):
    pass

class SalesTargetUpdate(SalesTargetBase):
    pass

class SalesTarget(SalesTargetBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class SalesForecast(BaseModel):
    period: str
    predicted_amount: float
    confidence: float  # 0-100
    factors: List[str]

# In a real implementation, these would connect to a database
# For now, we'll keep the in-memory storage but add configuration support
targets_db = [
    SalesTarget(
        id=1,
        name="Q1 2025 Sales Target",
        period="Q1 2025",
        target_amount=500000.0,
        assigned_to="John Sales",
        description="First quarter sales target for enterprise division",
        created_at=datetime.now()
    ),
    SalesTarget(
        id=2,
        name="Annual Sales Target",
        period="2025",
        target_amount=2000000.0,
        assigned_to="Sales Team",
        description="Annual sales target for the entire sales team",
        created_at=datetime.now()
    )
]

forecasts_db = [
    SalesForecast(
        period="Q1 2025",
        predicted_amount=450000.0,
        confidence=85.0,
        factors=["Market growth", "New product launch", "Seasonal trends"]
    ),
    SalesForecast(
        period="Q2 2025",
        predicted_amount=520000.0,
        confidence=78.0,
        factors=["Economic conditions", "Competitor activity", "Historical trends"]
    )
]

@router.get("/targets", response_model=List[SalesTarget])
def list_targets(organization_id: Optional[int] = None):
    """List all sales targets"""
    # In a real implementation, this would fetch from a database
    # For now, we return the in-memory data but could use organization_id for filtering
    return targets_db

@router.get("/targets/{target_id}", response_model=SalesTarget)
def get_target(target_id: int):
    """Get a specific sales target by ID"""
    for target in targets_db:
        if target.id == target_id:
            return target
    raise HTTPException(status_code=404, detail="Sales target not found")

@router.post("/targets", response_model=SalesTarget)
def create_target(target: SalesTargetCreate):
    """Create a new sales target"""
    new_id = max([t.id for t in targets_db]) + 1 if targets_db else 1
    new_target = SalesTarget(
        id=new_id,
        created_at=datetime.now(),
        **target.dict()
    )
    targets_db.append(new_target)
    return new_target

@router.put("/targets/{target_id}", response_model=SalesTarget)
def update_target(target_id: int, target_update: SalesTargetUpdate):
    """Update an existing sales target"""
    for index, target in enumerate(targets_db):
        if target.id == target_id:
            updated_target = SalesTarget(
                id=target_id,
                created_at=target.created_at,
                updated_at=datetime.now(),
                **target_update.dict()
            )
            targets_db[index] = updated_target
            return updated_target
    raise HTTPException(status_code=404, detail="Sales target not found")

@router.delete("/targets/{target_id}")
def delete_target(target_id: int):
    """Delete a sales target"""
    for index, target in enumerate(targets_db):
        if target.id == target_id:
            del targets_db[index]
            return {"message": "Sales target deleted successfully"}
    raise HTTPException(status_code=404, detail="Sales target not found")

@router.get("/forecasts", response_model=List[SalesForecast])
def list_forecasts(organization_id: Optional[int] = None):
    """List all sales forecasts"""
    # In a real implementation, this would fetch from a database
    # For now, we return the in-memory data but could use organization_id for filtering
    return forecasts_db

@router.get("/forecasts/current", response_model=SalesForecast)
def get_current_forecast():
    """Get the current sales forecast"""
    if forecasts_db:
        return forecasts_db[0]
    raise HTTPException(status_code=404, detail="No forecast available")

@router.get("/config/forecast_factors", response_model=List[str])
def get_forecast_factors(organization_id: Optional[int] = None):
    """
    Get available forecast factors from super admin configuration.
    Falls back to default values if super admin is unreachable.
    """
    return get_sales_config("forecast_factors", organization_id)

@router.get("/config/target_periods", response_model=List[str])
def get_target_periods(organization_id: Optional[int] = None):
    """
    Get available target periods from super admin configuration.
    Falls back to default values if super admin is unreachable.
    """
    return get_sales_config("target_periods", organization_id)