from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .models import (
    Asset, AssetCreate, AssetUpdate,
    Warranty, WarrantyCreate, WarrantyUpdate,
    Maintenance, MaintenanceCreate, MaintenanceUpdate
)
from .config import (
    get_asset_types, get_asset_statuses, get_warranty_statuses,
    get_default_asset_type, get_default_asset_status, get_maintenance_reminder_days
)

router = APIRouter()

# In-memory storage for demo purposes
assets_db = []
warranties_db = []
maintenance_db = []

@router.get("/", response_model=List[Asset])
def list_assets():
    """List all assets"""
    return assets_db

@router.get("/{asset_id}", response_model=Asset)
def get_asset(asset_id: int):
    """Get a specific asset by ID"""
    for asset in assets_db:
        if asset.id == asset_id:
            return asset
    raise HTTPException(status_code=404, detail="Asset not found")

@router.post("/", response_model=Asset)
def create_asset(asset: AssetCreate):
    """Create a new asset"""
    new_id = max([a.id for a in assets_db]) + 1 if assets_db else 1
    new_asset = Asset(
        id=new_id,
        created_at=datetime.now(),
        **asset.dict()
    )
    assets_db.append(new_asset)
    return new_asset

@router.put("/{asset_id}", response_model=Asset)
def update_asset(asset_id: int, asset_update: AssetUpdate):
    """Update an existing asset"""
    for index, asset in enumerate(assets_db):
        if asset.id == asset_id:
            updated_asset = Asset(
                id=asset_id,
                created_at=asset.created_at,
                updated_at=datetime.now(),
                **asset_update.dict()
            )
            assets_db[index] = updated_asset
            return updated_asset
    raise HTTPException(status_code=404, detail="Asset not found")

@router.delete("/{asset_id}")
def delete_asset(asset_id: int):
    """Delete an asset"""
    for index, asset in enumerate(assets_db):
        if asset.id == asset_id:
            del assets_db[index]
            return {"message": "Asset deleted successfully"}
    raise HTTPException(status_code=404, detail="Asset not found")

@router.get("/customer/{customer_id}", response_model=List[Asset])
def get_assets_by_customer(customer_id: int):
    """Get assets by customer ID"""
    return [asset for asset in assets_db if asset.assigned_to == customer_id]

@router.get("/type/{type}", response_model=List[Asset])
def get_assets_by_type(type: str):
    """Get assets by type"""
    # Normalize the type parameter to handle case differences
    normalized_type = type.lower().title()
    return [asset for asset in assets_db if asset.type.value == normalized_type]

@router.get("/status/{status}", response_model=List[Asset])
def get_assets_by_status(status: str):
    """Get assets by status"""
    # Normalize the status parameter to handle case differences
    normalized_status = status.lower().title()
    return [asset for asset in assets_db if asset.status.value == normalized_status]

@router.post("/{asset_id}/assign")
def assign_asset(asset_id: int, customer_id: int):
    """Assign an asset to a customer"""
    for index, asset in enumerate(assets_db):
        if asset.id == asset_id:
            assets_db[index].assigned_to = customer_id
            return {"message": "Asset assigned successfully"}
    raise HTTPException(status_code=404, detail="Asset not found")

@router.post("/{asset_id}/retire")
def retire_asset(asset_id: int):
    """Retire an asset"""
    for index, asset in enumerate(assets_db):
        if asset.id == asset_id:
            assets_db[index].status = "Retired"
            return {"message": "Asset retired successfully"}
    raise HTTPException(status_code=404, detail="Asset not found")

# Warranty endpoints
@router.get("/warranties", response_model=List[Warranty])
def list_warranties():
    """List all warranties"""
    return warranties_db

@router.get("/warranties/{warranty_id}", response_model=Warranty)
def get_warranty(warranty_id: int):
    """Get a specific warranty by ID"""
    for warranty in warranties_db:
        if warranty.id == warranty_id:
            return warranty
    raise HTTPException(status_code=404, detail="Warranty not found")

@router.post("/warranties", response_model=Warranty)
def create_warranty(warranty: WarrantyCreate):
    """Create a new warranty"""
    new_id = max([w.id for w in warranties_db]) + 1 if warranties_db else 1
    new_warranty = Warranty(
        id=new_id,
        created_at=datetime.now(),
        **warranty.dict()
    )
    warranties_db.append(new_warranty)
    return new_warranty

@router.put("/warranties/{warranty_id}", response_model=Warranty)
def update_warranty(warranty_id: int, warranty_update: WarrantyUpdate):
    """Update an existing warranty"""
    for index, warranty in enumerate(warranties_db):
        if warranty.id == warranty_id:
            updated_warranty = Warranty(
                id=warranty_id,
                created_at=warranty.created_at,
                updated_at=datetime.now(),
                **warranty_update.dict()
            )
            warranties_db[index] = updated_warranty
            return updated_warranty
    raise HTTPException(status_code=404, detail="Warranty not found")

@router.delete("/warranties/{warranty_id}")
def delete_warranty(warranty_id: int):
    """Delete a warranty"""
    for index, warranty in enumerate(warranties_db):
        if warranty.id == warranty_id:
            del warranties_db[index]
            return {"message": "Warranty deleted successfully"}
    raise HTTPException(status_code=404, detail="Warranty not found")

@router.get("/warranties/status/{status}", response_model=List[Warranty])
def get_warranties_by_status(status: str):
    """Get warranties by status"""
    # Normalize the status parameter to handle case differences
    normalized_status = status.lower().title()
    return [warranty for warranty in warranties_db if warranty.status.value == normalized_status]

@router.get("/assets/{asset_id}/warranty", response_model=Warranty)
def get_warranty_for_asset(asset_id: int):
    """Get warranty for a specific asset"""
    for warranty in warranties_db:
        if warranty.asset_id == asset_id:
            return warranty
    raise HTTPException(status_code=404, detail="Warranty not found")

@router.post("/warranties/{warranty_id}/void")
def void_warranty(warranty_id: int):
    """Void a warranty"""
    for index, warranty in enumerate(warranties_db):
        if warranty.id == warranty_id:
            warranties_db[index].status = "Void"
            return {"message": "Warranty voided successfully"}
    raise HTTPException(status_code=404, detail="Warranty not found")

# Maintenance endpoints
@router.get("/maintenance", response_model=List[Maintenance])
def list_maintenance():
    """List all maintenance records"""
    return maintenance_db

@router.get("/maintenance/{maintenance_id}", response_model=Maintenance)
def get_maintenance(maintenance_id: int):
    """Get a specific maintenance record by ID"""
    for maintenance in maintenance_db:
        if maintenance.id == maintenance_id:
            return maintenance
    raise HTTPException(status_code=404, detail="Maintenance record not found")

@router.post("/maintenance", response_model=Maintenance)
def create_maintenance(maintenance: MaintenanceCreate):
    """Create a new maintenance record"""
    new_id = max([m.id for m in maintenance_db]) + 1 if maintenance_db else 1
    new_maintenance = Maintenance(
        id=new_id,
        created_at=datetime.now(),
        **maintenance.dict()
    )
    maintenance_db.append(new_maintenance)
    return new_maintenance

@router.put("/maintenance/{maintenance_id}", response_model=Maintenance)
def update_maintenance(maintenance_id: int, maintenance_update: MaintenanceUpdate):
    """Update an existing maintenance record"""
    for index, maintenance in enumerate(maintenance_db):
        if maintenance.id == maintenance_id:
            updated_maintenance = Maintenance(
                id=maintenance_id,
                created_at=maintenance.created_at,
                updated_at=datetime.now(),
                **maintenance_update.dict()
            )
            maintenance_db[index] = updated_maintenance
            return updated_maintenance
    raise HTTPException(status_code=404, detail="Maintenance record not found")

@router.delete("/maintenance/{maintenance_id}")
def delete_maintenance(maintenance_id: int):
    """Delete a maintenance record"""
    for index, maintenance in enumerate(maintenance_db):
        if maintenance.id == maintenance_id:
            del maintenance_db[index]
            return {"message": "Maintenance record deleted successfully"}
    raise HTTPException(status_code=404, detail="Maintenance record not found")

@router.post("/maintenance/{maintenance_id}/complete")
def complete_maintenance(maintenance_id: int, cost: Optional[float] = None):
    """Mark a maintenance record as completed"""
    for index, maintenance in enumerate(maintenance_db):
        if maintenance.id == maintenance_id:
            maintenance_db[index].completed = True
            maintenance_db[index].completed_at = datetime.now()
            if cost is not None:
                maintenance_db[index].cost = cost
            return {"message": "Maintenance record marked as completed"}
    raise HTTPException(status_code=404, detail="Maintenance record not found")

@router.get("/assets/{asset_id}/maintenance", response_model=List[Maintenance])
def get_maintenance_for_asset(asset_id: int):
    """Get maintenance records for a specific asset"""
    return [maintenance for maintenance in maintenance_db if maintenance.asset_id == asset_id]

@router.get("/maintenance/pending", response_model=List[Maintenance])
def get_pending_maintenance():
    """Get all pending maintenance records"""
    return [maintenance for maintenance in maintenance_db if not maintenance.completed]

# Configuration endpoints
@router.get("/config/types", response_model=List[str])
def get_asset_type_options():
    """Get available asset type options"""
    return get_asset_types()

@router.get("/config/statuses", response_model=List[str])
def get_asset_status_options():
    """Get available asset status options"""
    return get_asset_statuses()

@router.get("/config/warranty-statuses", response_model=List[str])
def get_warranty_status_options():
    """Get available warranty status options"""
    return get_warranty_statuses()