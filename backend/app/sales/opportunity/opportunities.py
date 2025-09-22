from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime
from .models import (
    Opportunity, OpportunityCreate, OpportunityUpdate, OpportunityStage
)
from .config import (
    get_opportunity_stages, get_closed_won_stage
)

router = APIRouter()

# In-memory storage for demo purposes
opportunities_db = [
    Opportunity(
        id=1,
        name="Deal with Acme",
        description="Enterprise software package",
        value=100000.0,
        stage=OpportunityStage.proposal,
        probability=70,
        close_date=datetime.now(),
        account_id=1,
        contact_id=1,
        assigned_to="John Sales",
        notes="Custom integration required",
        created_at=datetime.now()
    ),
    Opportunity(
        id=2,
        name="Beta Expansion",
        description="Additional licenses for existing customer",
        value=50000.0,
        stage=OpportunityStage.negotiation,
        probability=90,
        close_date=datetime.now(),
        account_id=2,
        contact_id=2,
        assigned_to="Jane Sales",
        notes="Needs approval from finance team",
        created_at=datetime.now()
    )
]

@router.get("/", response_model=List[Opportunity])
def list_opportunities():
    return opportunities_db

@router.get("/{opportunity_id}", response_model=Opportunity)
def get_opportunity(opportunity_id: int):
    for opportunity in opportunities_db:
        if opportunity.id == opportunity_id:
            return opportunity
    raise HTTPException(status_code=404, detail="Opportunity not found")

@router.post("/", response_model=Opportunity)
def create_opportunity(opportunity: OpportunityCreate):
    new_id = max([o.id for o in opportunities_db]) + 1 if opportunities_db else 1
    new_opportunity = Opportunity(
        id=new_id,
        created_at=datetime.now(),
        **opportunity.dict()
    )
    opportunities_db.append(new_opportunity)
    return new_opportunity

@router.put("/{opportunity_id}", response_model=Opportunity)
def update_opportunity(opportunity_id: int, opportunity_update: OpportunityUpdate):
    for index, opportunity in enumerate(opportunities_db):
        if opportunity.id == opportunity_id:
            updated_opportunity = Opportunity(
                id=opportunity_id,
                created_at=opportunity.created_at,
                updated_at=datetime.now(),
                **opportunity_update.dict()
            )
            opportunities_db[index] = updated_opportunity
            return updated_opportunity
    raise HTTPException(status_code=404, detail="Opportunity not found")

@router.delete("/{opportunity_id}")
def delete_opportunity(opportunity_id: int):
    for index, opportunity in enumerate(opportunities_db):
        if opportunity.id == opportunity_id:
            del opportunities_db[index]
            return {"message": "Opportunity deleted successfully"}
    raise HTTPException(status_code=404, detail="Opportunity not found")

@router.get("/stage/{stage}", response_model=List[Opportunity])
def get_opportunities_by_stage(stage: str):
    """Get opportunities by stage"""
    return [opp for opp in opportunities_db if opp.stage.value.lower() == stage.lower()]

@router.get("/account/{account_id}", response_model=List[Opportunity])
def get_opportunities_by_account(account_id: int):
    """Get opportunities by account ID"""
    return [opp for opp in opportunities_db if opp.account_id == account_id]

@router.get("/contact/{contact_id}", response_model=List[Opportunity])
def get_opportunities_by_contact(contact_id: int):
    """Get opportunities by contact ID"""
    return [opp for opp in opportunities_db if opp.contact_id == contact_id]

@router.get("/assigned/{assigned_to}", response_model=List[Opportunity])
def get_opportunities_by_assignee(assigned_to: str):
    """Get opportunities by assignee"""
    return [opp for opp in opportunities_db if opp.assigned_to and opp.assigned_to.lower() == assigned_to.lower()]

@router.get("/value/{min_value}/{max_value}", response_model=List[Opportunity])
def get_opportunities_by_value_range(min_value: float, max_value: float):
    """Get opportunities by value range"""
    return [opp for opp in opportunities_db if min_value <= opp.value <= max_value]

@router.get("/probability/{min_probability}/{max_probability}", response_model=List[Opportunity])
def get_opportunities_by_probability_range(min_probability: int, max_probability: int):
    """Get opportunities by probability range"""
    return [opp for opp in opportunities_db if min_probability <= opp.probability <= max_probability]

@router.get("/recent/{days}", response_model=List[Opportunity])
def get_recent_opportunities(days: int):
    """Get opportunities created in the last N days"""
    from datetime import datetime, timedelta
    cutoff_date = datetime.now() - timedelta(days=days)
    return [opp for opp in opportunities_db if opp.created_at >= cutoff_date]

@router.get("/config/stages", response_model=List[str])
def get_opportunity_stage_options():
    """Get available opportunity stage options"""
    return get_opportunity_stages()

@router.get("/config/closed-won-stage", response_model=str)
def get_closed_won_stage_config():
    """Get the stage name for closed won opportunities"""
    return get_closed_won_stage()