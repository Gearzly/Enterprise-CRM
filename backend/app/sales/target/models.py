from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
# Import enums from the shared enums file
from app.models.enums import TargetPeriod, TargetType

class TargetBase(BaseModel):
    name: str
    description: Optional[str] = None
    target_type: TargetType
    period: TargetPeriod
    year: int
    target_value: float
    assigned_to: Optional[str] = None
    notes: Optional[str] = None

class TargetCreate(TargetBase):
    pass

class TargetUpdate(TargetBase):
    pass

class Target(TargetBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None