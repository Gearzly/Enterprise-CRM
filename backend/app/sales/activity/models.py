from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime

class ActivityBase(BaseModel):
    title: str
    description: Optional[str] = None
    activity_type: str
    status: str = "Pending"
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    related_to: Optional[str] = None  # Could be lead, contact, opportunity, etc.
    related_id: Optional[int] = None
    assigned_to: Optional[str] = None
    notes: Optional[str] = None

    @validator('activity_type')
    def validate_activity_type(cls, v):
        # In a real implementation, this would fetch from config
        # For now, we'll allow any string but validate against known values in the service layer
        return v

    @validator('status')
    def validate_status(cls, v):
        # In a real implementation, this would fetch from config
        # For now, we'll allow any string but validate against known values in the service layer
        return v

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(ActivityBase):
    pass

class Activity(ActivityBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None