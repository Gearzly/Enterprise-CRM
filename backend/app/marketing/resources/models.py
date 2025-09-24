from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime




class MarketingBudgetBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    allocated_amount: float
    spent_amount: float = 0.0
    start_date: datetime
    end_date: datetime
    status: str = "Draft"
    approver: Optional[str] = None
    notes: Optional[str] = None

class MarketingBudgetCreate(MarketingBudgetBase):
    pass

class MarketingBudgetUpdate(MarketingBudgetBase):
    pass

class MarketingBudget(MarketingBudgetBase):
    id: int
    remaining_amount: float = 0.0
    utilization_percentage: float = 0.0
    created_at: datetime
    updated_at: Optional[datetime] = None



class MarketingAssetBase(BaseModel):
    name: str
    description: Optional[str] = None
    asset_type: str
    file_url: str
    file_size: Optional[int] = None
    status: str = "Draft"
    tags: List[str] = []
    version: str = "1.0"
    owner: Optional[str] = None

class MarketingAssetCreate(MarketingAssetBase):
    pass

class MarketingAssetUpdate(MarketingAssetBase):
    pass

class MarketingAsset(MarketingAssetBase):
    id: int
    download_count: int = 0
    view_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

class ApprovalWorkflowBase(BaseModel):
    name: str
    description: Optional[str] = None
    asset_type: str
    approvers: List[str] = []  # List of user IDs or roles
    steps: List[Dict[str, Any]] = []  # JSON structure for workflow steps
    is_active: bool = True

class ApprovalWorkflowCreate(ApprovalWorkflowBase):
    pass

class ApprovalWorkflowUpdate(ApprovalWorkflowBase):
    pass

class ApprovalWorkflow(ApprovalWorkflowBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class VendorBase(BaseModel):
    name: str
    contact_person: str
    email: str
    phone: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    services: List[str] = []
    status: str = "Active"  # Active, Inactive, Suspended
    notes: Optional[str] = None

class VendorCreate(VendorBase):
    pass

class VendorUpdate(VendorBase):
    pass

class Vendor(VendorBase):
    id: int
    total_spent: float = 0.0
    project_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

class MarketingCalendarBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    activities: List[Dict[str, Any]] = []  # JSON structure for calendar activities
    is_public: bool = False
    tags: List[str] = []

class MarketingCalendarCreate(MarketingCalendarBase):
    pass

class MarketingCalendarUpdate(MarketingCalendarBase):
    pass

class MarketingCalendar(MarketingCalendarBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None