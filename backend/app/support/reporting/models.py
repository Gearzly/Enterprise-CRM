from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
# Removed Enum import since we're removing static enums

# Removed ReportType enum
# Removed ReportStatus enum
# Removed ReportFrequency enum

class ReportBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: str  # Changed from ReportType to str
    frequency: str  # Changed from ReportFrequency to str
    is_active: bool = True

class ReportCreate(ReportBase):
    pass

class ReportUpdate(ReportBase):
    pass

class Report(ReportBase):
    id: int
    status: str = "Pending"  # Changed from ReportStatus to str
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_generated_at: Optional[datetime] = None
    next_run_at: Optional[datetime] = None

class ReportDataPointBase(BaseModel):
    report_id: int
    timestamp: datetime
    data: Dict[str, Any]

class ReportDataPointCreate(ReportDataPointBase):
    pass

class ReportDataPoint(ReportDataPointBase):
    id: int

class DashboardBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool = False

class DashboardCreate(DashboardBase):
    pass

class DashboardUpdate(DashboardBase):
    pass

class Dashboard(DashboardBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class DashboardWidgetBase(BaseModel):
    dashboard_id: int
    title: str
    widget_type: str
    data_source: str
    config: Dict[str, Any] = {}

class DashboardWidgetCreate(DashboardWidgetBase):
    pass

class DashboardWidgetUpdate(DashboardWidgetBase):
    pass

class DashboardWidget(DashboardWidgetBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class MetricBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    unit: str
    is_active: bool = True

class MetricCreate(MetricBase):
    pass

class MetricUpdate(MetricBase):
    pass

class Metric(MetricBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None