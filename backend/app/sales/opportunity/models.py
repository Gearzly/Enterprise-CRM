from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class OpportunityStage(str, Enum):
    prospecting = "Prospecting"
    qualification = "Qualification"
    proposal = "Proposal"
    negotiation = "Negotiation"
    closed_won = "Closed Won"
    closed_lost = "Closed Lost"

class OpportunityBase(BaseModel):
    name: str
    description: Optional[str] = None
    value: float
    stage: OpportunityStage = OpportunityStage.prospecting
    probability: int = 0  # Percentage
    close_date: Optional[datetime] = None
    account_id: int
    contact_id: int
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