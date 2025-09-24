from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime

class QuotationBase(BaseModel):
    title: str
    description: Optional[str] = None
    opportunity_id: int
    account_id: int
    contact_id: int
    amount: float
    tax_amount: float = 0.0
    total_amount: float
    status: str = "Draft"
    valid_until: datetime
    notes: Optional[str] = None

    @validator('status')
    def validate_status(cls, v):
        # In a real implementation, this would fetch from config
        # For now, we'll allow any string but validate against known values in the service layer
        return v

class QuotationCreate(QuotationBase):
    pass

class QuotationUpdate(QuotationBase):
    pass

class Quotation(QuotationBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None