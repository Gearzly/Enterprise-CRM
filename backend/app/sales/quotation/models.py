from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class QuotationStatus(str, Enum):
    draft = "Draft"
    sent = "Sent"
    viewed = "Viewed"
    accepted = "Accepted"
    rejected = "Rejected"
    expired = "Expired"

class QuotationBase(BaseModel):
    title: str
    description: Optional[str] = None
    opportunity_id: int
    account_id: int
    contact_id: int
    amount: float
    tax_amount: float = 0.0
    total_amount: float
    status: QuotationStatus = QuotationStatus.draft
    valid_until: datetime
    notes: Optional[str] = None

class QuotationCreate(QuotationBase):
    pass

class QuotationUpdate(QuotationBase):
    pass

class Quotation(QuotationBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None