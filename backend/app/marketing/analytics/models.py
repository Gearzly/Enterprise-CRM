from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ReportType(str, Enum):
    campaign_performance = "Campaign Performance"
    lead_generation = "Lead Generation"
    email_marketing = "Email Marketing"
    social_media = "Social Media"
    content_performance = "Content Performance"
    roi_dashboard = "ROI Dashboard"
    conversion_tracking = "Conversion Tracking"
    attribution_modeling = "Attribution Modeling"
    customer_lifetime_value = "Customer Lifetime Value"
    channel_performance = "Channel Performance"

class ReportFrequency(str, Enum):
    daily = "Daily"
    weekly = "Weekly"
    monthly = "Monthly"
    quarterly = "Quarterly"
    yearly = "Yearly"
    custom = "Custom"

class AttributionModel(str, Enum):
    first_touch = "First Touch"
    last_touch = "Last Touch"
    linear = "Linear"
    time_decay = "Time Decay"
    u_shaped = "U-Shaped"
    w_shaped = "W-Shaped"

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
    report_type: ReportType
    frequency: ReportFrequency
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
    model_type: AttributionModel
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