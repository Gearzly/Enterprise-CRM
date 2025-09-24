from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AssetBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: str
    serial_number: Optional[str] = None
    model: Optional[str] = None
    manufacturer: Optional[str] = None
    purchase_date: Optional[datetime] = None
    purchase_price: Optional[float] = None
    assigned_to: Optional[int] = None  # customer_id
    status: str = "Active"
    tags: List[str] = []

class AssetCreate(AssetBase):
    pass

class AssetUpdate(AssetBase):
    pass

class Asset(AssetBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class WarrantyBase(BaseModel):
    asset_id: int
    provider: str
    start_date: datetime
    end_date: datetime
    coverage_details: Optional[str] = None
    status: str = "Active"

class WarrantyCreate(WarrantyBase):
    pass

class WarrantyUpdate(WarrantyBase):
    pass

class Warranty(WarrantyBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class MaintenanceBase(BaseModel):
    asset_id: int
    scheduled_date: datetime
    description: str
    completed: bool = False
    cost: Optional[float] = None

class MaintenanceCreate(MaintenanceBase):
    pass

class MaintenanceUpdate(MaintenanceBase):
    pass

class Maintenance(MaintenanceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None