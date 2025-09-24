from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime

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

    @validator('status')
    def validate_status(cls, v):
        # In a real implementation, this would fetch from config
        # For now, we'll allow any string but validate against known values in the service layer
        return v

    @validator('source')
    def validate_source(cls, v):
        # In a real implementation, this would fetch from config
        # For now, we'll allow any string but validate against known values in the service layer
        return v

class LeadCreate(LeadBase):
    pass

class LeadUpdate(LeadBase):
    pass

class Lead(LeadBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True