from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime
from .models import (
    Lead, LeadCreate, LeadUpdate, LeadStatus, LeadSource
)
from .config import (
    get_lead_statuses, get_lead_sources
)

router = APIRouter()

# In-memory storage for demo purposes
leads_db = [
    Lead(
        id=1,
        name="Acme Corp",
        company="Acme Corp",
        email="info@acme.com",
        phone="+1234567890",
        status=LeadStatus.new,
        source=LeadSource.website,
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
        status=LeadStatus.contacted,
        source=LeadSource.referral,
        assigned_to="Jane Sales",
        value=25000.0,
        notes="Needs custom features",
        created_at=datetime.now()
    )
]

@router.get("/", response_model=List[Lead])
def list_leads():
    return leads_db

@router.get("/{lead_id}", response_model=Lead)
def get_lead(lead_id: int):
    for lead in leads_db:
        if lead.id == lead_id:
            return lead
    raise HTTPException(status_code=404, detail="Lead not found")

@router.post("/", response_model=Lead)
def create_lead(lead: LeadCreate):
    new_id = max([l.id for l in leads_db]) + 1 if leads_db else 1
    new_lead = Lead(
        id=new_id,
        created_at=datetime.now(),
        **lead.dict()
    )
    leads_db.append(new_lead)
    return new_lead

@router.put("/{lead_id}", response_model=Lead)
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

@router.delete("/{lead_id}")
def delete_lead(lead_id: int):
    for index, lead in enumerate(leads_db):
        if lead.id == lead_id:
            del leads_db[index]
            return {"message": "Lead deleted successfully"}
    raise HTTPException(status_code=404, detail="Lead not found")

@router.get("/status/{status}", response_model=List[Lead])
def get_leads_by_status(status: str):
    """Get leads by status"""
    return [lead for lead in leads_db if lead.status.value.lower() == status.lower()]

@router.get("/source/{source}", response_model=List[Lead])
def get_leads_by_source(source: str):
    """Get leads by source"""
    return [lead for lead in leads_db if lead.source.value.lower() == source.lower()]

@router.get("/assigned/{assigned_to}", response_model=List[Lead])
def get_leads_by_assignee(assigned_to: str):
    """Get leads by assignee"""
    return [lead for lead in leads_db if lead.assigned_to and lead.assigned_to.lower() == assigned_to.lower()]

@router.get("/company/{company}", response_model=List[Lead])
def get_leads_by_company(company: str):
    """Get leads by company"""
    return [lead for lead in leads_db if lead.company.lower() == company.lower()]

@router.get("/value/{min_value}/{max_value}", response_model=List[Lead])
def get_leads_by_value_range(min_value: float, max_value: float):
    """Get leads by value range"""
    return [lead for lead in leads_db if lead.value and min_value <= lead.value <= max_value]

@router.get("/recent/{days}", response_model=List[Lead])
def get_recent_leads(days: int):
    """Get leads created in the last N days"""
    from datetime import datetime, timedelta
    cutoff_date = datetime.now() - timedelta(days=days)
    return [lead for lead in leads_db if lead.created_at >= cutoff_date]

@router.get("/config/statuses", response_model=List[str])
def get_lead_status_options():
    """Get available lead status options"""
    return get_lead_statuses()

@router.get("/config/sources", response_model=List[str])
def get_lead_source_options():
    """Get available lead source options"""
    return get_lead_sources()