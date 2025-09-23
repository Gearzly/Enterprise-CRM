from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .models import (
    Opportunity, OpportunityCreate, OpportunityUpdate, OpportunityStage
)
from .config import (
    get_opportunity_stages, get_closed_won_stage
)
from app.core.deps import get_db
from app.core.crud import opportunity as crud_opportunity

router = APIRouter()

@router.get("/", response_model=List[Opportunity])
def list_opportunities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all opportunities"""
    opportunities = crud_opportunity.get_multi(db, skip=skip, limit=limit)
    return opportunities

@router.get("/{opportunity_id}", response_model=Opportunity)
def get_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    """Get a specific opportunity by ID"""
    db_opportunity = crud_opportunity.get(db, id=opportunity_id)
    if db_opportunity is None:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return db_opportunity

@router.post("/", response_model=Opportunity)
def create_opportunity(opportunity: OpportunityCreate, db: Session = Depends(get_db)):
    """Create a new opportunity"""
    return crud_opportunity.create(db, obj_in=opportunity)

@router.put("/{opportunity_id}", response_model=Opportunity)
def update_opportunity(opportunity_id: int, opportunity_update: OpportunityUpdate, db: Session = Depends(get_db)):
    """Update an existing opportunity"""
    db_opportunity = crud_opportunity.get(db, id=opportunity_id)
    if db_opportunity is None:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return crud_opportunity.update(db, db_obj=db_opportunity, obj_in=opportunity_update)

@router.delete("/{opportunity_id}")
def delete_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    """Delete an opportunity"""
    db_opportunity = crud_opportunity.get(db, id=opportunity_id)
    if db_opportunity is None:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    crud_opportunity.remove(db, id=opportunity_id)
    return {"message": "Opportunity deleted successfully"}

@router.get("/stage/{stage}", response_model=List[Opportunity])
def get_opportunities_by_stage(stage: str, db: Session = Depends(get_db)):
    """Get opportunities by stage"""
    return crud_opportunity.get_by_stage(db, stage=stage)

@router.get("/account/{account_id}", response_model=List[Opportunity])
def get_opportunities_by_account(account_id: int, db: Session = Depends(get_db)):
    """Get opportunities by account ID"""
    return crud_opportunity.get_by_account(db, account_id=account_id)

@router.get("/contact/{contact_id}", response_model=List[Opportunity])
def get_opportunities_by_contact(contact_id: int, db: Session = Depends(get_db)):
    """Get opportunities by contact ID"""
    return crud_opportunity.get_by_contact(db, contact_id=contact_id)

@router.get("/assigned/{assigned_to}", response_model=List[Opportunity])
def get_opportunities_by_assignee(assigned_to: str, db: Session = Depends(get_db)):
    """Get opportunities by assignee"""
    return crud_opportunity.get_by_assigned_to(db, assigned_to=assigned_to)

@router.get("/value/{min_value}/{max_value}", response_model=List[Opportunity])
def get_opportunities_by_value_range(min_value: float, max_value: float, db: Session = Depends(get_db)):
    """Get opportunities by value range"""
    return crud_opportunity.get_multi_by_value_range(db, min_value=min_value, max_value=max_value)

@router.get("/probability/{min_probability}/{max_probability}", response_model=List[Opportunity])
def get_opportunities_by_probability_range(min_probability: int, max_probability: int, db: Session = Depends(get_db)):
    """Get opportunities by probability range"""
    return crud_opportunity.get_multi_by_probability_range(db, min_probability=min_probability, max_probability=max_probability)

@router.get("/recent/{days}", response_model=List[Opportunity])
def get_recent_opportunities(days: int, db: Session = Depends(get_db)):
    """Get opportunities created in the last N days"""
    return crud_opportunity.get_recent(db, days=days)

@router.get("/config/stages", response_model=List[str])
def get_opportunity_stage_options():
    """Get available opportunity stage options"""
    return get_opportunity_stages()

@router.get("/config/closed-won-stage", response_model=str)
def get_closed_won_stage_config():
    """Get the stage name for closed won opportunities"""
    return get_closed_won_stage()