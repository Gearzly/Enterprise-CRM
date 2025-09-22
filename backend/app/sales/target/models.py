from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class TargetPeriod(str, Enum):
    q1 = "Q1"
    q2 = "Q2"
    q3 = "Q3"
    q4 = "Q4"
    h1 = "H1"
    h2 = "H2"
    annual = "Annual"
    monthly = "Monthly"

class TargetType(str, Enum):
    revenue = "Revenue"
    leads = "Leads"
    opportunities = "Opportunities"
    conversions = "Conversions"

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