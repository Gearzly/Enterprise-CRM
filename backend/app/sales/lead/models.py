from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class LeadStatus(str, Enum):
    new = "New"
    contacted = "Contacted"
    qualified = "Qualified"
    unqualified = "Unqualified"
    converted = "Converted"

class LeadSource(str, Enum):
    website = "Website"
    referral = "Referral"
    social_media = "Social Media"
    email_campaign = "Email Campaign"
    event = "Event"
    other = "Other"

class LeadBase(BaseModel):
    name: str
    company: str
    email: Optional[str] = None
    phone: Optional[str] = None
    status: LeadStatus = LeadStatus.new
    source: LeadSource = LeadSource.website
    assigned_to: Optional[str] = None
    value: Optional[float] = None
    notes: Optional[str] = None

class LeadCreate(LeadBase):
    pass

class LeadUpdate(LeadBase):
    pass

class Lead(LeadBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None