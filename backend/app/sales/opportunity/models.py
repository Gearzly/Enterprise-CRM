from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
# Import enums from the shared enums file
from app.models.enums import OpportunityStage

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