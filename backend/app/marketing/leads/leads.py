from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from .models import (
    Lead, LeadCreate, LeadUpdate,
    LeadForm, LeadFormCreate, LeadFormUpdate,
    LeadScoreRule, LeadScoreRuleCreate, LeadScoreRuleUpdate,
    LeadAssignmentRule, LeadAssignmentRuleCreate, LeadAssignmentRuleUpdate
)
from .config import (
    get_lead_statuses, get_lead_sources,
    get_lead_score_rule_types, get_default_lead_score
)
from .service import LeadService, LeadFormService, LeadScoreRuleService, LeadAssignmentRuleService
from app.core.database import get_db

router = APIRouter(prefix="/leads", tags=["leads"])

# Initialize services
lead_service = LeadService()
lead_form_service = LeadFormService()
lead_score_rule_service = LeadScoreRuleService()
lead_assignment_rule_service = LeadAssignmentRuleService()

@router.get("/")
def get_leads_dashboard():
    """Get marketing leads dashboard with summary statistics"""
    return {
        "message": "Marketing Leads Dashboard",
        "statistics": {
            "total_leads": "Available via list endpoint",
            "leads_by_status": "Filtered by status",
            "lead_forms": "Available via forms endpoint",
            "scoring_rules": "Available via score-rules endpoint",
            "assignment_rules": "Available via assignment-rules endpoint"
        }
    }

@router.get("/", response_model=List[Lead])
def list_leads(db: Session = Depends(get_db)):
    """List all leads"""
    return lead_service.get_leads(db)

@router.get("/{lead_id}", response_model=Lead)
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    """Get a specific lead by ID"""
    lead = lead_service.get_lead(db, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

@router.post("/", response_model=Lead)
def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    """Create a new lead"""
    return lead_service.create_lead(db, lead)

@router.put("/{lead_id}", response_model=Lead)
def update_lead(lead_id: int, lead_update: LeadUpdate, db: Session = Depends(get_db)):
    """Update an existing lead"""
    lead = lead_service.update_lead(db, lead_id, lead_update)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

@router.delete("/{lead_id}")
def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    """Delete a lead"""
    success = lead_service.delete_lead(db, lead_id)
    if not success:
        raise HTTPException(status_code=404, detail="Lead not found")
    return {"message": "Lead deleted successfully"}

@router.get("/status/{status}", response_model=List[Lead])
def get_leads_by_status(status: str, db: Session = Depends(get_db)):
    """Get leads by status"""
    return lead_service.get_leads_by_status(db, status)

@router.get("/source/{source}", response_model=List[Lead])
def get_leads_by_source(source: str, db: Session = Depends(get_db)):
    """Get leads by source"""
    return lead_service.get_leads_by_source(db, source)

@router.get("/score/{min_score}/{max_score}", response_model=List[Lead])
def get_leads_by_score_range(min_score: int, max_score: int, db: Session = Depends(get_db)):
    """Get leads by score range"""
    return lead_service.get_leads_by_score_range(db, min_score, max_score)

# Lead Forms endpoints
@router.get("/forms", response_model=List[LeadForm])
def list_lead_forms(db: Session = Depends(get_db)):
    """List all lead forms"""
    return lead_form_service.get_forms(db)

@router.get("/forms/{form_id}", response_model=LeadForm)
def get_lead_form(form_id: int, db: Session = Depends(get_db)):
    """Get a specific lead form by ID"""
    form = lead_form_service.get_form(db, form_id)
    if not form:
        raise HTTPException(status_code=404, detail="Lead form not found")
    return form

@router.post("/forms", response_model=LeadForm)
def create_lead_form(form: LeadFormCreate, db: Session = Depends(get_db)):
    """Create a new lead form"""
    return lead_form_service.create_form(db, form)

@router.put("/forms/{form_id}", response_model=LeadForm)
def update_lead_form(form_id: int, form_update: LeadFormUpdate, db: Session = Depends(get_db)):
    """Update an existing lead form"""
    form = lead_form_service.update_form(db, form_id, form_update)
    if not form:
        raise HTTPException(status_code=404, detail="Lead form not found")
    return form

@router.delete("/forms/{form_id}")
def delete_lead_form(form_id: int, db: Session = Depends(get_db)):
    """Delete a lead form"""
    success = lead_form_service.delete_form(db, form_id)
    if not success:
        raise HTTPException(status_code=404, detail="Lead form not found")
    return {"message": "Lead form deleted successfully"}

# Lead Scoring Rules endpoints
@router.get("/score-rules", response_model=List[LeadScoreRule])
def list_lead_score_rules(db: Session = Depends(get_db)):
    """List all lead scoring rules"""
    return lead_score_rule_service.get_rules(db)

@router.get("/score-rules/{rule_id}", response_model=LeadScoreRule)
def get_lead_score_rule(rule_id: int, db: Session = Depends(get_db)):
    """Get a specific lead scoring rule by ID"""
    rule = lead_score_rule_service.get_rule(db, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Lead scoring rule not found")
    return rule

@router.post("/score-rules", response_model=LeadScoreRule)
def create_lead_score_rule(rule: LeadScoreRuleCreate, db: Session = Depends(get_db)):
    """Create a new lead scoring rule"""
    return lead_score_rule_service.create_rule(db, rule)

@router.put("/score-rules/{rule_id}", response_model=LeadScoreRule)
def update_lead_score_rule(rule_id: int, rule_update: LeadScoreRuleUpdate, db: Session = Depends(get_db)):
    """Update an existing lead scoring rule"""
    rule = lead_score_rule_service.update_rule(db, rule_id, rule_update)
    if not rule:
        raise HTTPException(status_code=404, detail="Lead scoring rule not found")
    return rule

@router.delete("/score-rules/{rule_id}")
def delete_lead_score_rule(rule_id: int, db: Session = Depends(get_db)):
    """Delete a lead scoring rule"""
    success = lead_score_rule_service.delete_rule(db, rule_id)
    if not success:
        raise HTTPException(status_code=404, detail="Lead scoring rule not found")
    return {"message": "Lead scoring rule deleted successfully"}

# Lead Assignment Rules endpoints
@router.get("/assignment-rules", response_model=List[LeadAssignmentRule])
def list_lead_assignment_rules(db: Session = Depends(get_db)):
    """List all lead assignment rules"""
    return lead_assignment_rule_service.get_rules(db)

@router.get("/assignment-rules/{rule_id}", response_model=LeadAssignmentRule)
def get_lead_assignment_rule(rule_id: int, db: Session = Depends(get_db)):
    """Get a specific lead assignment rule by ID"""
    rule = lead_assignment_rule_service.get_rule(db, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Lead assignment rule not found")
    return rule

@router.post("/assignment-rules", response_model=LeadAssignmentRule)
def create_lead_assignment_rule(rule: LeadAssignmentRuleCreate, db: Session = Depends(get_db)):
    """Create a new lead assignment rule"""
    return lead_assignment_rule_service.create_rule(db, rule)

@router.put("/assignment-rules/{rule_id}", response_model=LeadAssignmentRule)
def update_lead_assignment_rule(rule_id: int, rule_update: LeadAssignmentRuleUpdate, db: Session = Depends(get_db)):
    """Update an existing lead assignment rule"""
    rule = lead_assignment_rule_service.update_rule(db, rule_id, rule_update)
    if not rule:
        raise HTTPException(status_code=404, detail="Lead assignment rule not found")
    return rule

@router.delete("/assignment-rules/{rule_id}")
def delete_lead_assignment_rule(rule_id: int, db: Session = Depends(get_db)):
    """Delete a lead assignment rule"""
    success = lead_assignment_rule_service.delete_rule(db, rule_id)
    if not success:
        raise HTTPException(status_code=404, detail="Lead assignment rule not found")
    return {"message": "Lead assignment rule deleted successfully"}

# Configuration endpoints
@router.get("/config/statuses", response_model=List[str])
def get_lead_status_options():
    """Get available lead status options"""
    return get_lead_statuses()

@router.get("/config/sources", response_model=List[str])
def get_lead_source_options():
    """Get available lead source options"""
    return get_lead_sources()

@router.get("/config/score-rule-types", response_model=List[str])
def get_lead_score_rule_type_options():
    """Get available lead score rule types"""
    return get_lead_score_rule_types()