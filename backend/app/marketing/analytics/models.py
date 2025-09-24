from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class MarketingMetricBase(BaseModel):
    name: str
    value: float
    date: datetime
    campaign_id: Optional[int] = None
    channel: Optional[str] = None
    segment_id: Optional[int] = None

class MarketingMetricCreate(MarketingMetricBase):
    pass

class MarketingMetricUpdate(MarketingMetricBase):
    pass

class MarketingMetric(MarketingMetricBase):
    id: int
    created_at: datetime

class ReportBase(BaseModel):
    name: str
    description: Optional[str] = None
    report_type: str
    frequency: str
    is_active: bool = True
    filters: Dict[str, Any] = {}  # JSON structure for report filters
    recipients: List[str] = []  # Email addresses

class ReportCreate(ReportBase):
    pass

class ReportUpdate(ReportBase):
    pass

class Report(ReportBase):
    id: int
    last_generated_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

class DashboardBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool = False
    widgets: List[Dict[str, Any]] = []  # JSON structure for dashboard widgets

class DashboardCreate(DashboardBase):
    pass

class DashboardUpdate(DashboardBase):
    pass

class Dashboard(DashboardBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class ConversionTrackingBase(BaseModel):
    name: str
    description: Optional[str] = None
    conversion_type: str  # e.g., "form_submission", "purchase", "signup"
    tracking_code: str
    is_active: bool = True

class ConversionTrackingCreate(ConversionTrackingBase):
    pass

class ConversionTrackingUpdate(ConversionTrackingBase):
    pass

class ConversionTracking(ConversionTrackingBase):
    id: int
    conversion_count: int = 0
    conversion_rate: float = 0.0
    created_at: datetime
    updated_at: Optional[datetime] = None

class AttributionModelBase(BaseModel):
    name: str
    model_type: str
    description: Optional[str] = None
    is_default: bool = False
    settings: Dict[str, Any] = {}  # JSON structure for model settings

class AttributionModelCreate(AttributionModelBase):
    pass

class AttributionModelUpdate(AttributionModelBase):
    pass

class AttributionModel(AttributionModelBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None