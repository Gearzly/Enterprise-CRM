from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter()

class ContactBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    company: str
    position: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    pass

class Contact(ContactBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

# In-memory storage for demo purposes
contacts_db = [
    Contact(
        id=1,
        name="John Doe",
        email="john.doe@acme.com",
        phone="+1234567890",
        company="Acme Corp",
        position="CTO",
        address="123 Main St, New York, NY",
        notes="Interested in enterprise solution",
        created_at=datetime.now()
    ),
    Contact(
        id=2,
        name="Jane Smith",
        email="jane.smith@beta.com",
        phone="+1987654321",
        company="Beta Inc",
        position="Marketing Director",
        address="456 Market St, San Francisco, CA",
        notes="Looking for marketing automation tools",
        created_at=datetime.now()
    )
]

@router.get("/contacts", response_model=List[Contact])
def list_contacts():
    return contacts_db

@router.get("/contacts/{contact_id}", response_model=Contact)
def get_contact(contact_id: int):
    for contact in contacts_db:
        if contact.id == contact_id:
            return contact
    raise HTTPException(status_code=404, detail="Contact not found")

@router.post("/contacts", response_model=Contact)
def create_contact(contact: ContactCreate):
    new_id = max([c.id for c in contacts_db]) + 1 if contacts_db else 1
    new_contact = Contact(
        id=new_id,
        created_at=datetime.now(),
        **contact.dict()
    )
    contacts_db.append(new_contact)
    return new_contact

@router.put("/contacts/{contact_id}", response_model=Contact)
def update_contact(contact_id: int, contact_update: ContactUpdate):
    for index, contact in enumerate(contacts_db):
        if contact.id == contact_id:
            updated_contact = Contact(
                id=contact_id,
                created_at=contact.created_at,
                updated_at=datetime.now(),
                **contact_update.dict()
            )
            contacts_db[index] = updated_contact
            return updated_contact
    raise HTTPException(status_code=404, detail="Contact not found")

@router.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int):
    for index, contact in enumerate(contacts_db):
        if contact.id == contact_id:
            del contacts_db[index]
            return {"message": "Contact deleted successfully"}
    raise HTTPException(status_code=404, detail="Contact not found")