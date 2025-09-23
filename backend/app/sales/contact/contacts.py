from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .models import (
    Contact, ContactCreate, ContactUpdate, ContactType
)
from .config import (
    get_contact_types
)
from app.core.deps import get_db
from app.core.crud import contact as crud_contact

router = APIRouter()

@router.get("/", response_model=List[Contact])
def list_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all contacts"""
    contacts = crud_contact.get_multi(db, skip=skip, limit=limit)
    return contacts

@router.get("/{contact_id}", response_model=Contact)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    """Get a specific contact by ID"""
    db_contact = crud_contact.get(db, id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.post("/", response_model=Contact)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    """Create a new contact"""
    return crud_contact.create(db, obj_in=contact)

@router.put("/{contact_id}", response_model=Contact)
def update_contact(contact_id: int, contact_update: ContactUpdate, db: Session = Depends(get_db)):
    """Update an existing contact"""
    db_contact = crud_contact.get(db, id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return crud_contact.update(db, db_obj=db_contact, obj_in=contact_update)

@router.delete("/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    """Delete a contact"""
    db_contact = crud_contact.get(db, id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    crud_contact.remove(db, id=contact_id)
    return {"message": "Contact deleted successfully"}

@router.get("/type/{contact_type}", response_model=List[Contact])
def get_contacts_by_type(contact_type: str, db: Session = Depends(get_db)):
    """Get contacts by type"""
    return crud_contact.get_by_contact_type(db, contact_type=contact_type)

@router.get("/company/{company}", response_model=List[Contact])
def get_contacts_by_company(company: str, db: Session = Depends(get_db)):
    """Get contacts by company"""
    return crud_contact.get_by_company(db, company=company)

@router.get("/department/{department}", response_model=List[Contact])
def get_contacts_by_department(department: str, db: Session = Depends(get_db)):
    """Get contacts by department"""
    return crud_contact.get_by_department(db, department=department)

@router.get("/country/{country}", response_model=List[Contact])
def get_contacts_by_country(country: str, db: Session = Depends(get_db)):
    """Get contacts by country"""
    return crud_contact.get_by_country(db, country=country)

@router.get("/state/{state}", response_model=List[Contact])
def get_contacts_by_state(state: str, db: Session = Depends(get_db)):
    """Get contacts by state"""
    return crud_contact.get_by_state(db, state=state)

@router.get("/recent/{days}", response_model=List[Contact])
def get_recent_contacts(days: int, db: Session = Depends(get_db)):
    """Get contacts created in the last N days"""
    return crud_contact.get_recent(db, days=days)

@router.get("/config/types", response_model=List[str])
def get_contact_type_options():
    """Get available contact types"""
    return get_contact_types()