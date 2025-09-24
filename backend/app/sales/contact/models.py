from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    position: Optional[str] = None
    department: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    contact_type: str = "Primary"
    notes: Optional[str] = None

    @validator('contact_type')
    def validate_contact_type(cls, v):
        # In a real implementation, this would fetch from config
        # For now, we'll allow any string but validate against known values in the service layer
        return v

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    pass

class Contact(ContactBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True