from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime
from .models import (
    Contact, ContactCreate, ContactUpdate, ContactType
)
from .config import (
    get_contact_types
)

router = APIRouter()

# In-memory storage for demo purposes
contacts_db = [
    Contact(
        id=1,
        first_name="John",
        last_name="Doe",
        email="john.doe@acme.com",
        phone="+1234567890",
        company="Acme Corp",
        position="CTO",
        department="Engineering",
        address="123 Main St",
        city="New York",
        state="NY",
        country="USA",
        postal_code="10001",
        contact_type=ContactType.primary,
        notes="Interested in enterprise solution",
        created_at=datetime.now()
    ),
    Contact(
        id=2,
        first_name="Jane",
        last_name="Smith",
        email="jane.smith@beta.com",
        phone="+1987654321",
        company="Beta Inc",
        position="Marketing Director",
        department="Marketing",
        address="456 Market St",
        city="San Francisco",
        state="CA",
        country="USA",
        postal_code="94105",
        contact_type=ContactType.primary,
        notes="Looking for marketing automation tools",
        created_at=datetime.now()
    )
]

@router.get("/", response_model=List[Contact])
def list_contacts():
    return contacts_db

@router.get("/{contact_id}", response_model=Contact)
def get_contact(contact_id: int):
    for contact in contacts_db:
        if contact.id == contact_id:
            return contact
    raise HTTPException(status_code=404, detail="Contact not found")

@router.post("/", response_model=Contact)
def create_contact(contact: ContactCreate):
    new_id = max([c.id for c in contacts_db]) + 1 if contacts_db else 1
    new_contact = Contact(
        id=new_id,
        created_at=datetime.now(),
        **contact.dict()
    )
    contacts_db.append(new_contact)
    return new_contact

@router.put("/{contact_id}", response_model=Contact)
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

@router.delete("/{contact_id}")
def delete_contact(contact_id: int):
    for index, contact in enumerate(contacts_db):
        if contact.id == contact_id:
            del contacts_db[index]
            return {"message": "Contact deleted successfully"}
    raise HTTPException(status_code=404, detail="Contact not found")

@router.get("/type/{contact_type}", response_model=List[Contact])
def get_contacts_by_type(contact_type: str):
    """Get contacts by type"""
    return [contact for contact in contacts_db if contact.contact_type.value.lower() == contact_type.lower()]

@router.get("/company/{company}", response_model=List[Contact])
def get_contacts_by_company(company: str):
    """Get contacts by company"""
    return [contact for contact in contacts_db if contact.company.lower() == company.lower()]

@router.get("/department/{department}", response_model=List[Contact])
def get_contacts_by_department(department: str):
    """Get contacts by department"""
    return [contact for contact in contacts_db if contact.department and contact.department.lower() == department.lower()]

@router.get("/country/{country}", response_model=List[Contact])
def get_contacts_by_country(country: str):
    """Get contacts by country"""
    return [contact for contact in contacts_db if contact.country and contact.country.lower() == country.lower()]

@router.get("/state/{state}", response_model=List[Contact])
def get_contacts_by_state(state: str):
    """Get contacts by state"""
    return [contact for contact in contacts_db if contact.state and contact.state.lower() == state.lower()]

@router.get("/recent/{days}", response_model=List[Contact])
def get_recent_contacts(days: int):
    """Get contacts created in the last N days"""
    from datetime import datetime, timedelta
    cutoff_date = datetime.now() - timedelta(days=days)
    return [contact for contact in contacts_db if contact.created_at >= cutoff_date]

@router.get("/config/types", response_model=List[str])
def get_contact_type_options():
    """Get available contact types"""
    return get_contact_types()