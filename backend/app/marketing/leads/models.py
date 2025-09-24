from pydantic import BaseModel
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
    score: Optional[int] = 0
    notes: Optional[str] = None
    tags: List[str] = []

class LeadCreate(LeadBase):
    pass

class LeadUpdate(LeadBase):
    pass

class Lead(LeadBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class LeadFormBase(BaseModel):
    name: str
    title: str
    description: Optional[str] = None
    fields: List[dict]  # JSON structure for form fields
    is_active: bool = True
    redirect_url: Optional[str] = None

class LeadFormCreate(LeadFormBase):
    pass

class LeadFormUpdate(LeadFormBase):
    pass

class LeadForm(LeadFormBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class LeadScoreRuleBase(BaseModel):
    name: str
    description: Optional[str] = None
    rule_type: str
    criteria: dict  # JSON structure for scoring criteria
    points: int
    is_active: bool = True

class LeadScoreRuleCreate(LeadScoreRuleBase):
    pass

class LeadScoreRuleUpdate(LeadScoreRuleBase):
    pass

class LeadScoreRule(LeadScoreRuleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class LeadAssignmentRuleBase(BaseModel):
    name: str
    description: Optional[str] = None
    criteria: dict  # JSON structure for assignment criteria
    assign_to: str  # User or team to assign to
    is_active: bool = True

class LeadAssignmentRuleCreate(LeadAssignmentRuleBase):
    pass

class LeadAssignmentRuleUpdate(LeadAssignmentRuleBase):
    pass

class LeadAssignmentRule(LeadAssignmentRuleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None