from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .config import (
    get_lead_statuses, get_lead_sources
)

router = APIRouter()

class LeadBase(BaseModel):
    name: str
    company: str
    email: Optional[str] = None
    phone: Optional[str] = None
    status: str = "New"
    source: str = "Website"
    assigned_to: Optional[str] = None
    value: Optional[float] = None
    notes: Optional[str] = None

class LeadCreate(LeadBase):
    pass

class LeadUpdate(LeadBase):
    pass

class Lead(LeadBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

# In-memory storage for demo purposes
leads_db = [
    Lead(
        id=1,
        name="Acme Corp",
        company="Acme Corp",
        email="info@acme.com",
        phone="+1234567890",
        status="New",
        source="Website",
        assigned_to="John Sales",
        value=50000.0,
        notes="Interested in enterprise package",
        created_at=datetime.now()
    ),
    Lead(
        id=2,
        name="Beta Inc",
        company="Beta Inc",
        email="contact@beta.com",
        phone="+1987654321",
        status="Contacted",
        source="Referral",
        assigned_to="Jane Sales",
        value=25000.0,
        notes="Needs custom features",
        created_at=datetime.now()
    )
]

@router.get("/leads", response_model=List[Lead])
def list_leads():
    return leads_db

@router.get("/leads/{lead_id}", response_model=Lead)
def get_lead(lead_id: int):
    for lead in leads_db:
        if lead.id == lead_id:
            return lead
    raise HTTPException(status_code=404, detail="Lead not found")

@router.post("/leads", response_model=Lead)
def create_lead(lead: LeadCreate):
    new_id = max([l.id for l in leads_db]) + 1 if leads_db else 1
    new_lead = Lead(
        id=new_id,
        created_at=datetime.now(),
        **lead.dict()
    )
    leads_db.append(new_lead)
    return new_lead

@router.put("/leads/{lead_id}", response_model=Lead)
def update_lead(lead_id: int, lead_update: LeadUpdate):
    for index, lead in enumerate(leads_db):
        if lead.id == lead_id:
            updated_lead = Lead(
                id=lead_id,
                created_at=lead.created_at,
                updated_at=datetime.now(),
                **lead_update.dict()
            )
            leads_db[index] = updated_lead
            return updated_lead
    raise HTTPException(status_code=404, detail="Lead not found")

@router.delete("/leads/{lead_id}")
def delete_lead(lead_id: int):
    for index, lead in enumerate(leads_db):
        if lead.id == lead_id:
            del leads_db[index]
            return {"message": "Lead deleted successfully"}
    raise HTTPException(status_code=404, detail="Lead not found")

@router.get("/leads/status/{status}", response_model=List[Lead])
def get_leads_by_status(status: str):
    """Get leads by status"""
    # Normalize the status parameter to handle case differences
    normalized_status = status.lower().title()
    return [lead for lead in leads_db if lead.status == normalized_status]

@router.get("/config/statuses", response_model=List[str])
def get_lead_status_options():
    """Get available lead status options"""
    return get_lead_statuses()

@router.get("/config/sources", response_model=List[str])
def get_lead_source_options():
    """Get available lead source options"""
    return get_lead_sources()