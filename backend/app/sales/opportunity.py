from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .config import (
    get_opportunity_stages
)

router = APIRouter()

class OpportunityBase(BaseModel):
    name: str
    description: Optional[str] = None
    account_name: str
    contact_id: Optional[int] = None
    lead_id: Optional[int] = None
    stage: str = "Prospecting"
    probability: Optional[int] = None  # 0-100
    amount: Optional[float] = None
    expected_close_date: Optional[datetime] = None
    assigned_to: Optional[str] = None
    notes: Optional[str] = None

class OpportunityCreate(OpportunityBase):
    pass

class OpportunityUpdate(OpportunityBase):
    pass

class Opportunity(OpportunityBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

# In-memory storage for demo purposes
opportunities_db = [
    Opportunity(
        id=1,
        name="Deal with Acme",
        description="Enterprise software package",
        account_name="Acme Corp",
        contact_id=1,
        stage="Proposal",
        probability=70,
        amount=100000.0,
        expected_close_date=datetime.now(),
        assigned_to="John Sales",
        notes="Custom integration required",
        created_at=datetime.now()
    ),
    Opportunity(
        id=2,
        name="Beta Expansion",
        description="Additional licenses for existing customer",
        account_name="Beta Inc",
        contact_id=2,
        stage="Negotiation",
        probability=90,
        amount=50000.0,
        expected_close_date=datetime.now(),
        assigned_to="Jane Sales",
        notes="Needs approval from finance team",
        created_at=datetime.now()
    )
]

@router.get("/opportunities", response_model=List[Opportunity])
def list_opportunities():
    return opportunities_db

@router.get("/opportunities/{opportunity_id}", response_model=Opportunity)
def get_opportunity(opportunity_id: int):
    for opportunity in opportunities_db:
        if opportunity.id == opportunity_id:
            return opportunity
    raise HTTPException(status_code=404, detail="Opportunity not found")

@router.post("/opportunities", response_model=Opportunity)
def create_opportunity(opportunity: OpportunityCreate):
    new_id = max([o.id for o in opportunities_db]) + 1 if opportunities_db else 1
    new_opportunity = Opportunity(
        id=new_id,
        created_at=datetime.now(),
        **opportunity.dict()
    )
    opportunities_db.append(new_opportunity)
    return new_opportunity

@router.put("/opportunities/{opportunity_id}", response_model=Opportunity)
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

@router.delete("/opportunities/{opportunity_id}")
def delete_opportunity(opportunity_id: int):
    for index, opportunity in enumerate(opportunities_db):
        if opportunity.id == opportunity_id:
            del opportunities_db[index]
            return {"message": "Opportunity deleted successfully"}
    raise HTTPException(status_code=404, detail="Opportunity not found")

@router.get("/opportunities/stage/{stage}", response_model=List[Opportunity])
def get_opportunities_by_stage(stage: str):
    """Get opportunities by stage"""
    # Normalize the stage parameter to handle case differences
    normalized_stage = stage.lower().title()
    # Handle special case for "Closed Won" and "Closed Lost"
    if normalized_stage == "Closed Won":
        normalized_stage = "Closed Won"
    elif normalized_stage == "Closed Lost":
        normalized_stage = "Closed Lost"
    return [opp for opp in opportunities_db if opp.stage == normalized_stage]

@router.get("/config/stages", response_model=List[str])
def get_opportunity_stage_options():
    """Get available opportunity stage options"""
    return get_opportunity_stages()