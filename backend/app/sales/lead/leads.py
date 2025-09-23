from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .models import (
    Lead, LeadCreate, LeadUpdate, LeadStatus, LeadSource
)
from .config import (
    get_lead_statuses, get_lead_sources
)
from app.core.deps import get_db
from app.core.crud import lead as crud_lead

router = APIRouter()

@router.get("/", response_model=List[Lead])
def list_leads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all leads"""
    leads = crud_lead.get_multi(db, skip=skip, limit=limit)
    return leads

@router.get("/{lead_id}", response_model=Lead)
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    """Get a specific lead by ID"""
    db_lead = crud_lead.get(db, id=lead_id)
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return db_lead

@router.post("/", response_model=Lead)
def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    """Create a new lead"""
    return crud_lead.create(db, obj_in=lead)

@router.put("/{lead_id}", response_model=Lead)
def update_lead(lead_id: int, lead_update: LeadUpdate, db: Session = Depends(get_db)):
    """Update an existing lead"""
    db_lead = crud_lead.get(db, id=lead_id)
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return crud_lead.update(db, db_obj=db_lead, obj_in=lead_update)

@router.delete("/{lead_id}")
def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    """Delete a lead"""
    db_lead = crud_lead.get(db, id=lead_id)
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    crud_lead.remove(db, id=lead_id)
    return {"message": "Lead deleted successfully"}

@router.get("/status/{status}", response_model=List[Lead])
def get_leads_by_status(status: str, db: Session = Depends(get_db)):
    """Get leads by status"""
    return crud_lead.get_by_status(db, status=status)

@router.get("/source/{source}", response_model=List[Lead])
def get_leads_by_source(source: str, db: Session = Depends(get_db)):
    """Get leads by source"""
    return crud_lead.get_by_source(db, source=source)

@router.get("/assigned/{assigned_to}", response_model=List[Lead])
def get_leads_by_assignee(assigned_to: str, db: Session = Depends(get_db)):
    """Get leads by assignee"""
    return crud_lead.get_by_assigned_to(db, assigned_to=assigned_to)

@router.get("/company/{company}", response_model=List[Lead])
def get_leads_by_company(company: str, db: Session = Depends(get_db)):
    """Get leads by company"""
    return crud_lead.get_by_company(db, company=company)

@router.get("/value/{min_value}/{max_value}", response_model=List[Lead])
def get_leads_by_value_range(min_value: float, max_value: float, db: Session = Depends(get_db)):
    """Get leads by value range"""
    return crud_lead.get_multi_by_value_range(db, min_value=min_value, max_value=max_value)

@router.get("/recent/{days}", response_model=List[Lead])
def get_recent_leads(days: int, db: Session = Depends(get_db)):
    """Get leads created in the last N days"""
    return crud_lead.get_recent(db, days=days)

@router.get("/config/statuses", response_model=List[str])
def get_lead_status_options():
    """Get available lead status options"""
    return get_lead_statuses()

@router.get("/config/sources", response_model=List[str])
def get_lead_source_options():
    """Get available lead source options"""
    return get_lead_sources()