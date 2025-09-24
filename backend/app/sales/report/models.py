from pydantic import BaseModel, validator
from typing import List, Optional, Dict, Any
from datetime import datetime

class ReportBase(BaseModel):
    title: str
    description: Optional[str] = None
    report_type: str
    status: str = "Draft"
    generated_by: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None
    data: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None

    @validator('report_type')
    def validate_report_type(cls, v):
        # In a real implementation, this would fetch from config
        # For now, we'll allow any string but validate against known values in the service layer
        return v

    @validator('status')
    def validate_status(cls, v):
        # In a real implementation, this would fetch from config
        # For now, we'll allow any string but validate against known values in the service layer
        return v

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