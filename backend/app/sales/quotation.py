from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .config import (
    get_quotation_statuses, get_default_tax_rate
)

router = APIRouter()

class QuotationItemBase(BaseModel):
    description: str
    quantity: int
    unit_price: float
    total_price: float

class QuotationItemCreate(QuotationItemBase):
    pass

class QuotationItem(QuotationItemBase):
    id: int

class QuotationBase(BaseModel):
    customer_name: str
    customer_email: Optional[str] = None
    customer_address: Optional[str] = None
    opportunity_id: Optional[int] = None
    status: str = "Draft"
    issue_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    subtotal: float
    tax: Optional[float] = None  # Will be set from config if not provided
    total: float
    notes: Optional[str] = None
    terms: Optional[str] = None

class QuotationCreate(QuotationBase):
    items: List[QuotationItemCreate]

class QuotationUpdate(QuotationBase):
    items: List[QuotationItemCreate]

class Quotation(QuotationBase):
    id: int
    items: List[QuotationItem]
    created_at: datetime
    updated_at: Optional[datetime] = None

# In-memory storage for demo purposes
quotation_items_db = [
    QuotationItem(
        id=1,
        description="Software License - Annual",
        quantity=1,
        unit_price=50000.0,
        total_price=50000.0
    ),
    QuotationItem(
        id=2,
        description="Professional Services",
        quantity=10,
        unit_price=2000.0,
        total_price=20000.0
    )
]

quotations_db = [
    Quotation(
        id=1,
        customer_name="Acme Corp",
        customer_email="accounts@acme.com",
        customer_address="123 Main St, New York, NY",
        opportunity_id=1,
        status="Sent",
        issue_date=datetime.now(),
        expiry_date=datetime.now(),
        subtotal=70000.0,
        tax=7000.0,
        total=77000.0,
        notes="Special discount applied",
        terms="Net 30 days",
        items=[quotation_items_db[0]],
        created_at=datetime.now()
    ),
    Quotation(
        id=2,
        customer_name="Beta Inc",
        customer_email="finance@beta.com",
        customer_address="456 Market St, San Francisco, CA",
        opportunity_id=2,
        status="Draft",
        issue_date=datetime.now(),
        expiry_date=datetime.now(),
        subtotal=50000.0,
        tax=5000.0,
        total=55000.0,
        notes="Custom development package",
        terms="50% upfront, 50% upon delivery",
        items=[quotation_items_db[1]],
        created_at=datetime.now()
    )
]

@router.get("/quotations", response_model=List[Quotation])
def list_quotations():
    return quotations_db

@router.get("/quotations/{quotation_id}", response_model=Quotation)
def get_quotation(quotation_id: int):
    for quotation in quotations_db:
        if quotation.id == quotation_id:
            return quotation
    raise HTTPException(status_code=404, detail="Quotation not found")

@router.post("/quotations", response_model=Quotation)
def create_quotation(quotation: QuotationCreate):
    new_id = max([q.id for q in quotations_db]) + 1 if quotations_db else 1
    
    # Set default tax rate if not provided
    tax_rate = quotation.tax if quotation.tax is not None else get_default_tax_rate()
    
    # Create items with IDs
    items_with_ids = []
    for item in quotation.items:
        new_item_id = max([i.id for i in quotation_items_db]) + 1 if quotation_items_db else 1
        item_with_id = QuotationItem(id=new_item_id, **item.dict())
        quotation_items_db.append(item_with_id)
        items_with_ids.append(item_with_id)
    
    new_quotation = Quotation(
        id=new_id,
        items=items_with_ids,
        created_at=datetime.now(),
        tax=tax_rate,
        **quotation.dict(exclude={'items', 'tax'})
    )
    quotations_db.append(new_quotation)
    return new_quotation

@router.put("/quotations/{quotation_id}", response_model=Quotation)
def update_quotation(quotation_id: int, quotation_update: QuotationUpdate):
    for index, quotation in enumerate(quotations_db):
        if quotation.id == quotation_id:
            # Set default tax rate if not provided
            tax_rate = quotation_update.tax if quotation_update.tax is not None else get_default_tax_rate()
            
            # Create items with IDs
            items_with_ids = []
            for item in quotation_update.items:
                new_item_id = max([i.id for i in quotation_items_db]) + 1 if quotation_items_db else 1
                item_with_id = QuotationItem(id=new_item_id, **item.dict())
                quotation_items_db.append(item_with_id)
                items_with_ids.append(item_with_id)
            
            updated_quotation = Quotation(
                id=quotation_id,
                items=items_with_ids,
                created_at=quotation.created_at,
                updated_at=datetime.now(),
                tax=tax_rate,
                **quotation_update.dict(exclude={'items', 'tax'})
            )
            quotations_db[index] = updated_quotation
            return updated_quotation
    raise HTTPException(status_code=404, detail="Quotation not found")

@router.delete("/quotations/{quotation_id}")
def delete_quotation(quotation_id: int):
    for index, quotation in enumerate(quotations_db):
        if quotation.id == quotation_id:
            del quotations_db[index]
            return {"message": "Quotation deleted successfully"}
    raise HTTPException(status_code=404, detail="Quotation not found")

@router.get("/quotations/status/{status}", response_model=List[Quotation])
def get_quotations_by_status(status: str):
    """Get quotations by status"""
    # Normalize the status parameter to handle case differences
    normalized_status = status.lower().title()
    return [quotation for quotation in quotations_db if quotation.status == normalized_status]

@router.get("/config/statuses", response_model=List[str])
def get_quotation_status_options():
    """Get available quotation status options"""
    return get_quotation_statuses()