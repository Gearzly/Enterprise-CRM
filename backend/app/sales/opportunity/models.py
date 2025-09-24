from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime

class OpportunityBase(BaseModel):
    name: str
    description: Optional[str] = None
    value: float
    stage: str = "Prospecting"
    probability: int = 0  # Percentage
    close_date: Optional[datetime] = None
    account_id: int
    contact_id: int
    assigned_to: Optional[str] = None
    notes: Optional[str] = None

    @validator('stage')
    def validate_stage(cls, v):
        # In a real implementation, this would fetch from config
        # For now, we'll allow any string but validate against known values in the service layer
        return v

class OpportunityCreate(OpportunityBase):
    pass

class OpportunityUpdate(OpportunityBase):
    pass

class Opportunity(OpportunityBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True