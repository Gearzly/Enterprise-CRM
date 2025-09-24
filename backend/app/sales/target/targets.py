from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .models import (
    Target, TargetCreate, TargetUpdate
)
from .config import (
    get_target_periods, get_target_types
)
from app.core.deps import get_db
from app.core.crud import target as crud_target

router = APIRouter(prefix="/targets", tags=["targets"])

class SalesForecast(BaseModel):
    period: str
    predicted_amount: float
    confidence: float  # 0-100
    factors: List[str]

# In-memory storage for forecasts (these don't need to be in the database for now)
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

@router.get("/")
def get_targets_dashboard():
    """Get sales targets dashboard with summary statistics"""
    return {
        "message": "Sales Targets Dashboard",
        "statistics": {
            "total_targets": "Available via list endpoint",
            "targets_by_period": "Filtered by period",
            "targets_by_type": "Filtered by type",
            "forecasts": "Available via forecasts endpoint"
        }
    }

@router.get("/targets", response_model=List[Target])
def list_targets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all targets"""
    targets = crud_target.get_multi(db, skip=skip, limit=limit)
    return targets

@router.get("/{target_id}", response_model=Target)
def get_target(target_id: int, db: Session = Depends(get_db)):
    """Get a specific target by ID"""
    db_target = crud_target.get(db, id=target_id)
    if db_target is None:
        raise HTTPException(status_code=404, detail="Sales target not found")
    return db_target

@router.post("/", response_model=Target)
def create_target(target: TargetCreate, db: Session = Depends(get_db)):
    """Create a new target"""
    return crud_target.create(db, obj_in=target)

@router.put("/{target_id}", response_model=Target)
def update_target(target_id: int, target_update: TargetUpdate, db: Session = Depends(get_db)):
    """Update an existing target"""
    db_target = crud_target.get(db, id=target_id)
    if db_target is None:
        raise HTTPException(status_code=404, detail="Sales target not found")
    return crud_target.update(db, db_obj=db_target, obj_in=target_update)

@router.delete("/{target_id}")
def delete_target(target_id: int, db: Session = Depends(get_db)):
    """Delete a target"""
    db_target = crud_target.get(db, id=target_id)
    if db_target is None:
        raise HTTPException(status_code=404, detail="Sales target not found")
    crud_target.remove(db, id=target_id)
    return {"message": "Sales target deleted successfully"}

@router.get("/period/{period}", response_model=List[Target])
def get_targets_by_period(period: str, db: Session = Depends(get_db)):
    """Get targets by period"""
    return crud_target.get_by_period(db, period=period)

@router.get("/type/{target_type}", response_model=List[Target])
def get_targets_by_type(target_type: str, db: Session = Depends(get_db)):
    """Get targets by type"""
    return crud_target.get_by_type(db, target_type=target_type)

@router.get("/year/{year}", response_model=List[Target])
def get_targets_by_year(year: int, db: Session = Depends(get_db)):
    """Get targets by year"""
    return crud_target.get_by_year(db, year=year)

@router.get("/assigned/{assigned_to}", response_model=List[Target])
def get_targets_by_assignee(assigned_to: str, db: Session = Depends(get_db)):
    """Get targets by assignee"""
    return crud_target.get_by_assigned_to(db, assigned_to=assigned_to)

@router.get("/value/{min_value}/{max_value}", response_model=List[Target])
def get_targets_by_value_range(min_value: float, max_value: float, db: Session = Depends(get_db)):
    """Get targets by value range"""
    return crud_target.get_multi_by_value_range(db, min_value=min_value, max_value=max_value)

@router.get("/upcoming", response_model=List[Target])
def get_upcoming_targets(db: Session = Depends(get_db)):
    """Get upcoming targets for the current and next year"""
    current_year = datetime.now().year
    return crud_target.get_by_year(db, year=current_year)

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