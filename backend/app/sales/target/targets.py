from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from .models import (
    Target, TargetCreate, TargetUpdate, TargetType, TargetPeriod
)
from .config import (
    get_target_periods, get_target_types
)

router = APIRouter()

class SalesForecast(BaseModel):
    period: str
    predicted_amount: float
    confidence: float  # 0-100
    factors: List[str]

# In-memory storage for demo purposes
targets_db = [
    Target(
        id=1,
        name="Q1 2025 Sales Target",
        description="First quarter sales target for enterprise division",
        target_type=TargetType.revenue,
        period=TargetPeriod.q1,
        year=2025,
        target_value=500000.0,
        assigned_to="John Sales",
        created_at=datetime.now()
    ),
    Target(
        id=2,
        name="Annual Sales Target",
        description="Annual sales target for the entire sales team",
        target_type=TargetType.revenue,
        period=TargetPeriod.annual,
        year=2025,
        target_value=2000000.0,
        assigned_to="Sales Team",
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

@router.get("/", response_model=List[Target])
def list_targets():
    return targets_db

@router.get("/{target_id}", response_model=Target)
def get_target(target_id: int):
    for target in targets_db:
        if target.id == target_id:
            return target
    raise HTTPException(status_code=404, detail="Sales target not found")

@router.post("/", response_model=Target)
def create_target(target: TargetCreate):
    new_id = max([t.id for t in targets_db]) + 1 if targets_db else 1
    new_target = Target(
        id=new_id,
        created_at=datetime.now(),
        **target.dict()
    )
    targets_db.append(new_target)
    return new_target

@router.put("/{target_id}", response_model=Target)
def update_target(target_id: int, target_update: TargetUpdate):
    for index, target in enumerate(targets_db):
        if target.id == target_id:
            updated_target = Target(
                id=target_id,
                created_at=target.created_at,
                updated_at=datetime.now(),
                **target_update.dict()
            )
            targets_db[index] = updated_target
            return updated_target
    raise HTTPException(status_code=404, detail="Sales target not found")

@router.delete("/{target_id}")
def delete_target(target_id: int):
    for index, target in enumerate(targets_db):
        if target.id == target_id:
            del targets_db[index]
            return {"message": "Sales target deleted successfully"}
    raise HTTPException(status_code=404, detail="Sales target not found")

@router.get("/period/{period}", response_model=List[Target])
def get_targets_by_period(period: str):
    """Get targets by period"""
    return [target for target in targets_db if target.period.value.lower() == period.lower()]

@router.get("/type/{target_type}", response_model=List[Target])
def get_targets_by_type(target_type: str):
    """Get targets by type"""
    return [target for target in targets_db if target.target_type.value.lower() == target_type.lower()]

@router.get("/year/{year}", response_model=List[Target])
def get_targets_by_year(year: int):
    """Get targets by year"""
    return [target for target in targets_db if target.year == year]

@router.get("/assigned/{assigned_to}", response_model=List[Target])
def get_targets_by_assignee(assigned_to: str):
    """Get targets by assignee"""
    return [target for target in targets_db if target.assigned_to and target.assigned_to.lower() == assigned_to.lower()]

@router.get("/value/{min_value}/{max_value}", response_model=List[Target])
def get_targets_by_value_range(min_value: float, max_value: float):
    """Get targets by value range"""
    return [target for target in targets_db if min_value <= target.target_value <= max_value]

@router.get("/upcoming", response_model=List[Target])
def get_upcoming_targets():
    """Get upcoming targets for the current and next year"""
    from datetime import datetime
    current_year = datetime.now().year
    return [target for target in targets_db if target.year >= current_year]

@router.get("/forecasts", response_model=List[SalesForecast])
def list_forecasts():
    """List all sales forecasts"""
    return forecasts_db

@router.get("/forecasts/current", response_model=SalesForecast)
def get_current_forecast():
    """Get the current sales forecast"""
    if forecasts_db:
        return forecasts_db[0]
    raise HTTPException(status_code=404, detail="No forecast available")

@router.get("/config/periods", response_model=List[str])
def get_target_period_options():
    """Get available target periods"""
    return get_target_periods()

@router.get("/config/types", response_model=List[str])
def get_target_type_options():
    """Get available target types"""
    return get_target_types()