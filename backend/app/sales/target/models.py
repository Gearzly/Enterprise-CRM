from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime

class TargetBase(BaseModel):
    name: str
    description: Optional[str] = None
    target_type: str
    period: str
    year: int
    target_value: float
    assigned_to: Optional[str] = None
    notes: Optional[str] = None

    @validator('target_type')
    def validate_target_type(cls, v):
        # In a real implementation, this would fetch from config
        # For now, we'll allow any string but validate against known values in the service layer
        return v

    @validator('period')
    def validate_period(cls, v):
        # In a real implementation, this would fetch from config
        # For now, we'll allow any string but validate against known values in the service layer
        return v

class TargetCreate(TargetBase):
    pass

class TargetUpdate(TargetBase):
    pass

class Target(TargetBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None