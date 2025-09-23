from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
# Import enums from the shared enums file
from app.models.enums import ReportType, ReportStatus

class ReportBase(BaseModel):
    title: str
    description: Optional[str] = None
    report_type: ReportType
    status: ReportStatus = ReportStatus.draft
    generated_by: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None
    data: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None

class ReportCreate(ReportBase):
    pass

class ReportUpdate(ReportBase):
    pass

class Report(ReportBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    generated_at: Optional[datetime] = None

# Additional models for sales reporting
class SalesMetrics(BaseModel):
    total_leads: int
    total_opportunities: int
    total_quotations: int
    total_sales: float
    deals_closed: int
    conversion_rate: float

class LeadByStatus(BaseModel):
    status: str
    count: int

class OpportunityByStage(BaseModel):
    stage: str
    count: int
    total_value: float

class QuotationByStatus(BaseModel):
    status: str
    count: int
    total_value: float

class SalesReport(BaseModel):
    metrics: SalesMetrics
    leads_by_status: List[LeadByStatus]
    opportunities_by_stage: List[OpportunityByStage]
    quotations_by_status: List[QuotationByStatus]