from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .models import (
    Quotation, QuotationCreate, QuotationUpdate
)
from .config import (
    get_quotation_statuses, get_default_tax_rate
)
from app.core.deps import get_db
from app.core.crud import quotation as crud_quotation

router = APIRouter(prefix="/quotations", tags=["quotations"])

@router.get("/")
def get_quotations_dashboard():
    """Get sales quotations dashboard with summary statistics"""
    return {
        "message": "Sales Quotations Dashboard",
        "statistics": {
            "total_quotations": "Available via list endpoint",
            "quotations_by_status": "Filtered by status",
            "quotations_by_amount": "Filtered by amount range",
            "recent_quotations": "Available via recent endpoint"
        }
    }

@router.get("/quotations", response_model=List[Quotation])
def list_quotations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all quotations"""
    quotations = crud_quotation.get_multi(db, skip=skip, limit=limit)
    return quotations

@router.get("/{quotation_id}", response_model=Quotation)
def get_quotation(quotation_id: int, db: Session = Depends(get_db)):
    """Get a specific quotation by ID"""
    db_quotation = crud_quotation.get(db, id=quotation_id)
    if db_quotation is None:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return db_quotation

@router.post("/", response_model=Quotation)
def create_quotation(quotation: QuotationCreate, db: Session = Depends(get_db)):
    """Create a new quotation"""
    # Set default tax rate if not provided
    if quotation.tax_amount is None:
        quotation.tax_amount = get_default_tax_rate()
    return crud_quotation.create(db, obj_in=quotation)

@router.put("/{quotation_id}", response_model=Quotation)
def update_quotation(quotation_id: int, quotation_update: QuotationUpdate, db: Session = Depends(get_db)):
    """Update an existing quotation"""
    db_quotation = crud_quotation.get(db, id=quotation_id)
    if db_quotation is None:
        raise HTTPException(status_code=404, detail="Quotation not found")
    # Set default tax rate if not provided
    if quotation_update.tax_amount is None:
        quotation_update.tax_amount = get_default_tax_rate()
    return crud_quotation.update(db, db_obj=db_quotation, obj_in=quotation_update)

@router.delete("/{quotation_id}")
def delete_quotation(quotation_id: int, db: Session = Depends(get_db)):
    """Delete a quotation"""
    db_quotation = crud_quotation.get(db, id=quotation_id)
    if db_quotation is None:
        raise HTTPException(status_code=404, detail="Quotation not found")
    crud_quotation.remove(db, id=quotation_id)
    return {"message": "Quotation deleted successfully"}

@router.get("/status/{status}", response_model=List[Quotation])
def get_quotations_by_status(status: str, db: Session = Depends(get_db)):
    """Get quotations by status"""
    return crud_quotation.get_by_status(db, status=status)

@router.get("/account/{account_id}", response_model=List[Quotation])
def get_quotations_by_account(account_id: int, db: Session = Depends(get_db)):
    """Get quotations by account ID"""
    return crud_quotation.get_by_account(db, account_id=account_id)

@router.get("/contact/{contact_id}", response_model=List[Quotation])
def get_quotations_by_contact(contact_id: int, db: Session = Depends(get_db)):
    """Get quotations by contact ID"""
    return crud_quotation.get_by_contact(db, contact_id=contact_id)

@router.get("/opportunity/{opportunity_id}", response_model=List[Quotation])
def get_quotations_by_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    """Get quotations by opportunity ID"""
    return crud_quotation.get_by_opportunity(db, opportunity_id=opportunity_id)

@router.get("/amount/{min_amount}/{max_amount}", response_model=List[Quotation])
def get_quotations_by_amount_range(min_amount: float, max_amount: float, db: Session = Depends(get_db)):
    """Get quotations by amount range"""
    return crud_quotation.get_multi_by_amount_range(db, min_amount=min_amount, max_amount=max_amount)

@router.get("/valid-until/{days}", response_model=List[Quotation])
def get_quotations_valid_within_days(days: int, db: Session = Depends(get_db)):
    """Get quotations valid within the next N days"""
    return crud_quotation.get_valid_within_days(db, days=days)

@router.get("/recent/{days}", response_model=List[Quotation])
def get_recent_quotations(days: int, db: Session = Depends(get_db)):
    """Get quotations created in the last N days"""
    return crud_quotation.get_recent(db, days=days)

@router.get("/config/statuses", response_model=List[str])
def get_quotation_status_options():
    """Get available quotation status options"""
    return get_quotation_statuses()

@router.get("/config/default-tax-rate", response_model=float)
def get_default_tax_rate_config():
    """Get default tax rate"""
    return get_default_tax_rate()