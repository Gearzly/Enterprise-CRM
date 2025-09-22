from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class BudgetStatus(str, Enum):
    draft = "Draft"
    approved = "Approved"
    active = "Active"
    completed = "Completed"
    cancelled = "Cancelled"

class BudgetCategory(str, Enum):
    campaigns = "Campaigns"
    content = "Content"
    events = "Events"
    technology = "Technology"
    personnel = "Personnel"
    agency = "Agency Fees"
    other = "Other"

class MarketingBudgetBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: BudgetCategory
    allocated_amount: float
    spent_amount: float = 0.0
    start_date: datetime
    end_date: datetime
    status: BudgetStatus = BudgetStatus.draft
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

class AssetType(str, Enum):
    image = "Image"
    video = "Video"
    document = "Document"
    template = "Template"
    brand_asset = "Brand Asset"
    other = "Other"

class AssetStatus(str, Enum):
    draft = "Draft"
    review = "Review"
    approved = "Approved"
    published = "Published"
    archived = "Archived"

class MarketingAssetBase(BaseModel):
    name: str
    description: Optional[str] = None
    asset_type: AssetType
    file_url: str
    file_size: Optional[int] = None
    status: AssetStatus = AssetStatus.draft
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
    asset_type: AssetType
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