from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class ContactType(str, Enum):
    primary = "Primary"
    secondary = "Secondary"
    billing = "Billing"
    shipping = "Shipping"

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    company: str
    position: Optional[str] = None
    department: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    contact_type: ContactType = ContactType.primary
    notes: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    pass

class Contact(ContactBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None