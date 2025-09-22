from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum
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

router = APIRouter()

# In-memory storage for demo purposes
leads_db = []
lead_forms_db = []
lead_score_rules_db = []
lead_assignment_rules_db = []

@router.get("/", response_model=List[Lead])
def list_leads():
    """List all leads"""
    return leads_db

@router.get("/{lead_id}", response_model=Lead)
def get_lead(lead_id: int):
    """Get a specific lead by ID"""
    for lead in leads_db:
        if lead.id == lead_id:
            return lead
    raise HTTPException(status_code=404, detail="Lead not found")

@router.post("/", response_model=Lead)
def create_lead(lead: LeadCreate):
    """Create a new lead"""
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
    """Update an existing lead"""
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
    """Delete a lead"""
    for index, lead in enumerate(leads_db):
        if lead.id == lead_id:
            del leads_db[index]
            return {"message": "Lead deleted successfully"}
    raise HTTPException(status_code=404, detail="Lead not found")

@router.get("/status/{status}", response_model=List[Lead])
def get_leads_by_status(status: str):
    """Get leads by status"""
    # Normalize the status parameter to handle case differences
    normalized_status = status.lower().title()
    return [lead for lead in leads_db if lead.status.value == normalized_status]

@router.get("/source/{source}", response_model=List[Lead])
def get_leads_by_source(source: str):
    """Get leads by source"""
    # Normalize the source parameter to handle case differences
    normalized_source = source.lower().title()
    return [lead for lead in leads_db if lead.source.value == normalized_source]

@router.get("/score/{min_score}/{max_score}", response_model=List[Lead])
def get_leads_by_score_range(min_score: int, max_score: int):
    """Get leads by score range"""
    return [lead for lead in leads_db if min_score <= lead.score <= max_score]

# Lead Forms endpoints
@router.get("/forms", response_model=List[LeadForm])
def list_lead_forms():
    """List all lead forms"""
    return lead_forms_db

@router.get("/forms/{form_id}", response_model=LeadForm)
def get_lead_form(form_id: int):
    """Get a specific lead form by ID"""
    for form in lead_forms_db:
        if form.id == form_id:
            return form
    raise HTTPException(status_code=404, detail="Lead form not found")

@router.post("/forms", response_model=LeadForm)
def create_lead_form(form: LeadFormCreate):
    """Create a new lead form"""
    new_id = max([f.id for f in lead_forms_db]) + 1 if lead_forms_db else 1
    new_form = LeadForm(
        id=new_id,
        created_at=datetime.now(),
        **form.dict()
    )
    lead_forms_db.append(new_form)
    return new_form

@router.put("/forms/{form_id}", response_model=LeadForm)
def update_lead_form(form_id: int, form_update: LeadFormUpdate):
    """Update an existing lead form"""
    for index, form in enumerate(lead_forms_db):
        if form.id == form_id:
            updated_form = LeadForm(
                id=form_id,
                created_at=form.created_at,
                updated_at=datetime.now(),
                **form_update.dict()
            )
            lead_forms_db[index] = updated_form
            return updated_form
    raise HTTPException(status_code=404, detail="Lead form not found")

@router.delete("/forms/{form_id}")
def delete_lead_form(form_id: int):
    """Delete a lead form"""
    for index, form in enumerate(lead_forms_db):
        if form.id == form_id:
            del lead_forms_db[index]
            return {"message": "Lead form deleted successfully"}
    raise HTTPException(status_code=404, detail="Lead form not found")

# Lead Scoring Rules endpoints
@router.get("/score-rules", response_model=List[LeadScoreRule])
def list_lead_score_rules():
    """List all lead scoring rules"""
    return lead_score_rules_db

@router.get("/score-rules/{rule_id}", response_model=LeadScoreRule)
def get_lead_score_rule(rule_id: int):
    """Get a specific lead scoring rule by ID"""
    for rule in lead_score_rules_db:
        if rule.id == rule_id:
            return rule
    raise HTTPException(status_code=404, detail="Lead scoring rule not found")

@router.post("/score-rules", response_model=LeadScoreRule)
def create_lead_score_rule(rule: LeadScoreRuleCreate):
    """Create a new lead scoring rule"""
    new_id = max([r.id for r in lead_score_rules_db]) + 1 if lead_score_rules_db else 1
    new_rule = LeadScoreRule(
        id=new_id,
        created_at=datetime.now(),
        **rule.dict()
    )
    lead_score_rules_db.append(new_rule)
    return new_rule

@router.put("/score-rules/{rule_id}", response_model=LeadScoreRule)
def update_lead_score_rule(rule_id: int, rule_update: LeadScoreRuleUpdate):
    """Update an existing lead scoring rule"""
    for index, rule in enumerate(lead_score_rules_db):
        if rule.id == rule_id:
            updated_rule = LeadScoreRule(
                id=rule_id,
                created_at=rule.created_at,
                updated_at=datetime.now(),
                **rule_update.dict()
            )
            lead_score_rules_db[index] = updated_rule
            return updated_rule
    raise HTTPException(status_code=404, detail="Lead scoring rule not found")

@router.delete("/score-rules/{rule_id}")
def delete_lead_score_rule(rule_id: int):
    """Delete a lead scoring rule"""
    for index, rule in enumerate(lead_score_rules_db):
        if rule.id == rule_id:
            del lead_score_rules_db[index]
            return {"message": "Lead scoring rule deleted successfully"}
    raise HTTPException(status_code=404, detail="Lead scoring rule not found")

# Lead Assignment Rules endpoints
@router.get("/assignment-rules", response_model=List[LeadAssignmentRule])
def list_lead_assignment_rules():
    """List all lead assignment rules"""
    return lead_assignment_rules_db

@router.get("/assignment-rules/{rule_id}", response_model=LeadAssignmentRule)
def get_lead_assignment_rule(rule_id: int):
    """Get a specific lead assignment rule by ID"""
    for rule in lead_assignment_rules_db:
        if rule.id == rule_id:
            return rule
    raise HTTPException(status_code=404, detail="Lead assignment rule not found")

@router.post("/assignment-rules", response_model=LeadAssignmentRule)
def create_lead_assignment_rule(rule: LeadAssignmentRuleCreate):
    """Create a new lead assignment rule"""
    new_id = max([r.id for r in lead_assignment_rules_db]) + 1 if lead_assignment_rules_db else 1
    new_rule = LeadAssignmentRule(
        id=new_id,
        created_at=datetime.now(),
        **rule.dict()
    )
    lead_assignment_rules_db.append(new_rule)
    return new_rule

@router.put("/assignment-rules/{rule_id}", response_model=LeadAssignmentRule)
def update_lead_assignment_rule(rule_id: int, rule_update: LeadAssignmentRuleUpdate):
    """Update an existing lead assignment rule"""
    for index, rule in enumerate(lead_assignment_rules_db):
        if rule.id == rule_id:
            updated_rule = LeadAssignmentRule(
                id=rule_id,
                created_at=rule.created_at,
                updated_at=datetime.now(),
                **rule_update.dict()
            )
            lead_assignment_rules_db[index] = updated_rule
            return updated_rule
    raise HTTPException(status_code=404, detail="Lead assignment rule not found")

@router.delete("/assignment-rules/{rule_id}")
def delete_lead_assignment_rule(rule_id: int):
    """Delete a lead assignment rule"""
    for index, rule in enumerate(lead_assignment_rules_db):
        if rule.id == rule_id:
            del lead_assignment_rules_db[index]
            return {"message": "Lead assignment rule deleted successfully"}
    raise HTTPException(status_code=404, detail="Lead assignment rule not found")

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