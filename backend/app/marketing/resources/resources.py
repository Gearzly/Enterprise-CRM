from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from .models import (
    MarketingBudget, MarketingBudgetCreate, MarketingBudgetUpdate,
    MarketingAsset, MarketingAssetCreate, MarketingAssetUpdate,
    ApprovalWorkflow, ApprovalWorkflowCreate, ApprovalWorkflowUpdate,
    Vendor, VendorCreate, VendorUpdate,
    MarketingCalendar, MarketingCalendarCreate, MarketingCalendarUpdate
)
from .config import (
    get_budget_statuses, get_budget_categories,
    get_asset_types, get_asset_statuses,
    get_default_utilization_percentage
)

router = APIRouter()

# In-memory storage for demo purposes
marketing_budgets_db = []
marketing_assets_db = []
approval_workflows_db = []
vendors_db = []
marketing_calendars_db = []

@router.get("/budgets", response_model=List[MarketingBudget])
def list_marketing_budgets():
    """List all marketing budgets"""
    return marketing_budgets_db

@router.get("/budgets/{budget_id}", response_model=MarketingBudget)
def get_marketing_budget(budget_id: int):
    """Get a specific marketing budget by ID"""
    for budget in marketing_budgets_db:
        if budget.id == budget_id:
            return budget
    raise HTTPException(status_code=404, detail="Marketing budget not found")

@router.post("/budgets", response_model=MarketingBudget)
def create_marketing_budget(budget: MarketingBudgetCreate):
    """Create a new marketing budget"""
    new_id = max([b.id for b in marketing_budgets_db]) + 1 if marketing_budgets_db else 1
    remaining_amount = budget.allocated_amount - budget.spent_amount
    utilization_percentage = (budget.spent_amount / budget.allocated_amount * 100) if budget.allocated_amount > 0 else 0.0
    
    new_budget = MarketingBudget(
        id=new_id,
        created_at=datetime.now(),
        remaining_amount=remaining_amount,
        utilization_percentage=utilization_percentage,
        **budget.dict()
    )
    marketing_budgets_db.append(new_budget)
    return new_budget

@router.put("/budgets/{budget_id}", response_model=MarketingBudget)
def update_marketing_budget(budget_id: int, budget_update: MarketingBudgetUpdate):
    """Update an existing marketing budget"""
    for index, budget in enumerate(marketing_budgets_db):
        if budget.id == budget_id:
            remaining_amount = budget.allocated_amount - budget.spent_amount
            utilization_percentage = (budget.spent_amount / budget.allocated_amount * 100) if budget.allocated_amount > 0 else 0.0
            
            updated_budget = MarketingBudget(
                id=budget_id,
                created_at=budget.created_at,
                updated_at=datetime.now(),
                remaining_amount=remaining_amount,
                utilization_percentage=utilization_percentage,
                **budget_update.dict()
            )
            marketing_budgets_db[index] = updated_budget
            return updated_budget
    raise HTTPException(status_code=404, detail="Marketing budget not found")

@router.delete("/budgets/{budget_id}")
def delete_marketing_budget(budget_id: int):
    """Delete a marketing budget"""
    for index, budget in enumerate(marketing_budgets_db):
        if budget.id == budget_id:
            del marketing_budgets_db[index]
            return {"message": "Marketing budget deleted successfully"}
    raise HTTPException(status_code=404, detail="Marketing budget not found")

@router.get("/budgets/status/{status}", response_model=List[MarketingBudget])
def get_marketing_budgets_by_status(status: str):
    """Get marketing budgets by status"""
    # Normalize the status parameter to handle case differences
    normalized_status = status.lower().title()
    return [budget for budget in marketing_budgets_db if budget.status == normalized_status]

@router.get("/budgets/category/{category}", response_model=List[MarketingBudget])
def get_marketing_budgets_by_category(category: str):
    """Get marketing budgets by category"""
    # Normalize the category parameter to handle case differences
    normalized_category = category.lower().title()
    return [budget for budget in marketing_budgets_db if budget.category == normalized_category]

@router.post("/budgets/{budget_id}/approve")
def approve_marketing_budget(budget_id: int):
    """Approve a marketing budget"""
    for index, budget in enumerate(marketing_budgets_db):
        if budget.id == budget_id:
            budget.status = "Approved"
            budget.approver = "System"
            budget.updated_at = datetime.now()
            marketing_budgets_db[index] = budget
            return {"message": f"Marketing budget {budget_id} approved"}
    raise HTTPException(status_code=404, detail="Marketing budget not found")

# Marketing Assets endpoints
@router.get("/assets", response_model=List[MarketingAsset])
def list_marketing_assets():
    """List all marketing assets"""
    return marketing_assets_db

@router.get("/assets/{asset_id}", response_model=MarketingAsset)
def get_marketing_asset(asset_id: int):
    """Get a specific marketing asset by ID"""
    for asset in marketing_assets_db:
        if asset.id == asset_id:
            return asset
    raise HTTPException(status_code=404, detail="Marketing asset not found")

@router.post("/assets", response_model=MarketingAsset)
def create_marketing_asset(asset: MarketingAssetCreate):
    """Create a new marketing asset"""
    new_id = max([a.id for a in marketing_assets_db]) + 1 if marketing_assets_db else 1
    new_asset = MarketingAsset(
        id=new_id,
        created_at=datetime.now(),
        download_count=0,
        view_count=0,
        **asset.dict()
    )
    marketing_assets_db.append(new_asset)
    return new_asset

@router.put("/assets/{asset_id}", response_model=MarketingAsset)
def update_marketing_asset(asset_id: int, asset_update: MarketingAssetUpdate):
    """Update an existing marketing asset"""
    for index, asset in enumerate(marketing_assets_db):
        if asset.id == asset_id:
            updated_asset = MarketingAsset(
                id=asset_id,
                created_at=asset.created_at,
                updated_at=datetime.now(),
                download_count=asset.download_count,
                view_count=asset.view_count,
                **asset_update.dict()
            )
            marketing_assets_db[index] = updated_asset
            return updated_asset
    raise HTTPException(status_code=404, detail="Marketing asset not found")

@router.delete("/assets/{asset_id}")
def delete_marketing_asset(asset_id: int):
    """Delete a marketing asset"""
    for index, asset in enumerate(marketing_assets_db):
        if asset.id == asset_id:
            del marketing_assets_db[index]
            return {"message": "Marketing asset deleted successfully"}
    raise HTTPException(status_code=404, detail="Marketing asset not found")

@router.get("/assets/type/{asset_type}", response_model=List[MarketingAsset])
def get_marketing_assets_by_type(asset_type: str):
    """Get marketing assets by type"""
    # Normalize the asset_type parameter to handle case differences
    normalized_type = asset_type.lower().title()
    return [asset for asset in marketing_assets_db if asset.asset_type == normalized_type]

@router.get("/assets/status/{status}", response_model=List[MarketingAsset])
def get_marketing_assets_by_status(status: str):
    """Get marketing assets by status"""
    # Normalize the status parameter to handle case differences
    normalized_status = status.lower().title()
    return [asset for asset in marketing_assets_db if asset.status == normalized_status]

@router.post("/assets/{asset_id}/download")
def download_marketing_asset(asset_id: int):
    """Record a download of a marketing asset"""
    for index, asset in enumerate(marketing_assets_db):
        if asset.id == asset_id:
            asset.download_count += 1
            asset.updated_at = datetime.now()
            marketing_assets_db[index] = asset
            return {"message": f"Marketing asset {asset_id} downloaded"}
    raise HTTPException(status_code=404, detail="Marketing asset not found")

@router.post("/assets/{asset_id}/view")
def view_marketing_asset(asset_id: int):
    """Record a view of a marketing asset"""
    for index, asset in enumerate(marketing_assets_db):
        if asset.id == asset_id:
            asset.view_count += 1
            asset.updated_at = datetime.now()
            marketing_assets_db[index] = asset
            return {"message": f"Marketing asset {asset_id} viewed"}
    raise HTTPException(status_code=404, detail="Marketing asset not found")

# Approval Workflows endpoints
@router.get("/approval-workflows", response_model=List[ApprovalWorkflow])
def list_approval_workflows():
    """List all approval workflows"""
    return approval_workflows_db

@router.get("/approval-workflows/{workflow_id}", response_model=ApprovalWorkflow)
def get_approval_workflow(workflow_id: int):
    """Get a specific approval workflow by ID"""
    for workflow in approval_workflows_db:
        if workflow.id == workflow_id:
            return workflow
    raise HTTPException(status_code=404, detail="Approval workflow not found")

@router.post("/approval-workflows", response_model=ApprovalWorkflow)
def create_approval_workflow(workflow: ApprovalWorkflowCreate):
    """Create a new approval workflow"""
    new_id = max([w.id for w in approval_workflows_db]) + 1 if approval_workflows_db else 1
    new_workflow = ApprovalWorkflow(
        id=new_id,
        created_at=datetime.now(),
        **workflow.dict()
    )
    approval_workflows_db.append(new_workflow)
    return new_workflow

@router.put("/approval-workflows/{workflow_id}", response_model=ApprovalWorkflow)
def update_approval_workflow(workflow_id: int, workflow_update: ApprovalWorkflowUpdate):
    """Update an existing approval workflow"""
    for index, workflow in enumerate(approval_workflows_db):
        if workflow.id == workflow_id:
            updated_workflow = ApprovalWorkflow(
                id=workflow_id,
                created_at=workflow.created_at,
                updated_at=datetime.now(),
                **workflow_update.dict()
            )
            approval_workflows_db[index] = updated_workflow
            return updated_workflow
    raise HTTPException(status_code=404, detail="Approval workflow not found")

@router.delete("/approval-workflows/{workflow_id}")
def delete_approval_workflow(workflow_id: int):
    """Delete an approval workflow"""
    for index, workflow in enumerate(approval_workflows_db):
        if workflow.id == workflow_id:
            del approval_workflows_db[index]
            return {"message": "Approval workflow deleted successfully"}
    raise HTTPException(status_code=404, detail="Approval workflow not found")

# Vendors endpoints
@router.get("/vendors", response_model=List[Vendor])
def list_vendors():
    """List all vendors"""
    return vendors_db

@router.get("/vendors/{vendor_id}", response_model=Vendor)
def get_vendor(vendor_id: int):
    """Get a specific vendor by ID"""
    for vendor in vendors_db:
        if vendor.id == vendor_id:
            return vendor
    raise HTTPException(status_code=404, detail="Vendor not found")

@router.post("/vendors", response_model=Vendor)
def create_vendor(vendor: VendorCreate):
    """Create a new vendor"""
    new_id = max([v.id for v in vendors_db]) + 1 if vendors_db else 1
    new_vendor = Vendor(
        id=new_id,
        created_at=datetime.now(),
        total_spent=0.0,
        project_count=0,
        **vendor.dict()
    )
    vendors_db.append(new_vendor)
    return new_vendor

@router.put("/vendors/{vendor_id}", response_model=Vendor)
def update_vendor(vendor_id: int, vendor_update: VendorUpdate):
    """Update an existing vendor"""
    for index, vendor in enumerate(vendors_db):
        if vendor.id == vendor_id:
            updated_vendor = Vendor(
                id=vendor_id,
                created_at=vendor.created_at,
                updated_at=datetime.now(),
                total_spent=vendor.total_spent,
                project_count=vendor.project_count,
                **vendor_update.dict()
            )
            vendors_db[index] = updated_vendor
            return updated_vendor
    raise HTTPException(status_code=404, detail="Vendor not found")

@router.delete("/vendors/{vendor_id}")
def delete_vendor(vendor_id: int):
    """Delete a vendor"""
    for index, vendor in enumerate(vendors_db):
        if vendor.id == vendor_id:
            del vendors_db[index]
            return {"message": "Vendor deleted successfully"}
    raise HTTPException(status_code=404, detail="Vendor not found")

@router.post("/vendors/{vendor_id}/suspend")
def suspend_vendor(vendor_id: int):
    """Suspend a vendor"""
    for index, vendor in enumerate(vendors_db):
        if vendor.id == vendor_id:
            vendor.status = "Suspended"
            vendor.updated_at = datetime.now()
            vendors_db[index] = vendor
            return {"message": f"Vendor {vendor_id} suspended"}
    raise HTTPException(status_code=404, detail="Vendor not found")

# Marketing Calendars endpoints
@router.get("/calendars", response_model=List[MarketingCalendar])
def list_marketing_calendars():
    """List all marketing calendars"""
    return marketing_calendars_db

@router.get("/calendars/{calendar_id}", response_model=MarketingCalendar)
def get_marketing_calendar(calendar_id: int):
    """Get a specific marketing calendar by ID"""
    for calendar in marketing_calendars_db:
        if calendar.id == calendar_id:
            return calendar
    raise HTTPException(status_code=404, detail="Marketing calendar not found")

@router.post("/calendars", response_model=MarketingCalendar)
def create_marketing_calendar(calendar: MarketingCalendarCreate):
    """Create a new marketing calendar"""
    new_id = max([c.id for c in marketing_calendars_db]) + 1 if marketing_calendars_db else 1
    new_calendar = MarketingCalendar(
        id=new_id,
        created_at=datetime.now(),
        **calendar.dict()
    )
    marketing_calendars_db.append(new_calendar)
    return new_calendar

@router.put("/calendars/{calendar_id}", response_model=MarketingCalendar)
def update_marketing_calendar(calendar_id: int, calendar_update: MarketingCalendarUpdate):
    """Update an existing marketing calendar"""
    for index, calendar in enumerate(marketing_calendars_db):
        if calendar.id == calendar_id:
            updated_calendar = MarketingCalendar(
                id=calendar_id,
                created_at=calendar.created_at,
                updated_at=datetime.now(),
                **calendar_update.dict()
            )
            marketing_calendars_db[index] = updated_calendar
            return updated_calendar
    raise HTTPException(status_code=404, detail="Marketing calendar not found")

@router.delete("/calendars/{calendar_id}")
def delete_marketing_calendar(calendar_id: int):
    """Delete a marketing calendar"""
    for index, calendar in enumerate(marketing_calendars_db):
        if calendar.id == calendar_id:
            del marketing_calendars_db[index]
            return {"message": "Marketing calendar deleted successfully"}
    raise HTTPException(status_code=404, detail="Marketing calendar not found")

# Configuration endpoints
@router.get("/config/budget-statuses", response_model=List[str])
def get_budget_status_options():
    """Get available budget statuses"""
    return get_budget_statuses()

@router.get("/config/budget-categories", response_model=List[str])
def get_budget_category_options():
    """Get available budget categories"""
    return get_budget_categories()

@router.get("/config/asset-types", response_model=List[str])
def get_asset_type_options():
    """Get available asset types"""
    return get_asset_types()

@router.get("/config/asset-statuses", response_model=List[str])
def get_asset_status_options():
    """Get available asset statuses"""
    return get_asset_statuses()