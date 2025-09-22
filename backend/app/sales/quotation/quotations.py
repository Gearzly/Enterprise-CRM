from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime
from .models import (
    Quotation, QuotationCreate, QuotationUpdate, QuotationStatus
)
from .config import (
    get_quotation_statuses, get_default_tax_rate
)

router = APIRouter()

# In-memory storage for demo purposes
quotation_items_db = [
    {
        "id": 1,
        "description": "Software License - Annual",
        "quantity": 1,
        "unit_price": 50000.0,
        "total_price": 50000.0
    },
    {
        "id": 2,
        "description": "Professional Services",
        "quantity": 10,
        "unit_price": 2000.0,
        "total_price": 20000.0
    }
]

quotations_db = [
    Quotation(
        id=1,
        title="Software License for Acme Corp",
        description="Annual software license and support",
        opportunity_id=1,
        account_id=1,
        contact_id=1,
        amount=70000.0,
        tax_amount=7000.0,
        total_amount=77000.0,
        status=QuotationStatus.sent,
        valid_until=datetime.now(),
        notes="Special discount applied",
        created_at=datetime.now()
    ),
    Quotation(
        id=2,
        title="Services for Beta Inc",
        description="Custom development package",
        opportunity_id=2,
        account_id=2,
        contact_id=2,
        amount=50000.0,
        tax_amount=5000.0,
        total_amount=55000.0,
        status=QuotationStatus.draft,
        valid_until=datetime.now(),
        notes="Custom development package",
        created_at=datetime.now()
    )
]

@router.get("/", response_model=List[Quotation])
def list_quotations():
    return quotations_db

@router.get("/{quotation_id}", response_model=Quotation)
def get_quotation(quotation_id: int):
    for quotation in quotations_db:
        if quotation.id == quotation_id:
            return quotation
    raise HTTPException(status_code=404, detail="Quotation not found")

@router.post("/", response_model=Quotation)
def create_quotation(quotation: QuotationCreate):
    new_id = max([q.id for q in quotations_db]) + 1 if quotations_db else 1
    
    # Set default tax rate if not provided
    tax_rate = quotation.tax_amount if quotation.tax_amount is not None else get_default_tax_rate()
    
    new_quotation = Quotation(
        id=new_id,
        created_at=datetime.now(),
        tax_amount=tax_rate,
        **quotation.dict()
    )
    quotations_db.append(new_quotation)
    return new_quotation

@router.put("/{quotation_id}", response_model=Quotation)
def update_quotation(quotation_id: int, quotation_update: QuotationUpdate):
    for index, quotation in enumerate(quotations_db):
        if quotation.id == quotation_id:
            # Set default tax rate if not provided
            tax_rate = quotation_update.tax_amount if quotation_update.tax_amount is not None else get_default_tax_rate()
            
            updated_quotation = Quotation(
                id=quotation_id,
                created_at=quotation.created_at,
                updated_at=datetime.now(),
                tax_amount=tax_rate,
                **quotation_update.dict()
            )
            quotations_db[index] = updated_quotation
            return updated_quotation
    raise HTTPException(status_code=404, detail="Quotation not found")

@router.delete("/{quotation_id}")
def delete_quotation(quotation_id: int):
    for index, quotation in enumerate(quotations_db):
        if quotation.id == quotation_id:
            del quotations_db[index]
            return {"message": "Quotation deleted successfully"}
    raise HTTPException(status_code=404, detail="Quotation not found")

@router.get("/status/{status}", response_model=List[Quotation])
def get_quotations_by_status(status: str):
    """Get quotations by status"""
    return [quotation for quotation in quotations_db if quotation.status.value.lower() == status.lower()]

@router.get("/account/{account_id}", response_model=List[Quotation])
def get_quotations_by_account(account_id: int):
    """Get quotations by account ID"""
    return [quotation for quotation in quotations_db if quotation.account_id == account_id]

@router.get("/contact/{contact_id}", response_model=List[Quotation])
def get_quotations_by_contact(contact_id: int):
    """Get quotations by contact ID"""
    return [quotation for quotation in quotations_db if quotation.contact_id == contact_id]

@router.get("/opportunity/{opportunity_id}", response_model=List[Quotation])
def get_quotations_by_opportunity(opportunity_id: int):
    """Get quotations by opportunity ID"""
    return [quotation for quotation in quotations_db if quotation.opportunity_id == opportunity_id]

@router.get("/amount/{min_amount}/{max_amount}", response_model=List[Quotation])
def get_quotations_by_amount_range(min_amount: float, max_amount: float):
    """Get quotations by amount range"""
    return [quotation for quotation in quotations_db if min_amount <= quotation.total_amount <= max_amount]

@router.get("/valid-until/{days}", response_model=List[Quotation])
def get_quotations_valid_within_days(days: int):
    """Get quotations valid within the next N days"""
    from datetime import datetime, timedelta
    cutoff_date = datetime.now() + timedelta(days=days)
    return [quotation for quotation in quotations_db if quotation.valid_until <= cutoff_date]

@router.get("/recent/{days}", response_model=List[Quotation])
def get_recent_quotations(days: int):
    """Get quotations created in the last N days"""
    from datetime import datetime, timedelta
    cutoff_date = datetime.now() - timedelta(days=days)
    return [quotation for quotation in quotations_db if quotation.created_at >= cutoff_date]

@router.get("/config/statuses", response_model=List[str])
def get_quotation_status_options():
    """Get available quotation status options"""
    return get_quotation_statuses()

@router.get("/config/default-tax-rate", response_model=float)
def get_default_tax_rate_config():
    """Get default tax rate"""
    return get_default_tax_rate()