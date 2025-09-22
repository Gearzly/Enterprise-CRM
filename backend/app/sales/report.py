from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .lead import leads_db
from .opportunity import opportunities_db
from .quotation import quotations_db
from .config import get_closed_won_stage

router = APIRouter()

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

@router.get("/reports/sales", response_model=SalesReport)
def sales_report():
    # Get the closed won stage from config
    closed_won_stage = get_closed_won_stage()
    
    # Calculate total sales and deals closed
    total_sales = sum([opp.amount or 0 for opp in opportunities_db if opp.stage == closed_won_stage])
    deals_closed = len([opp for opp in opportunities_db if opp.stage == closed_won_stage])
    
    # Calculate total leads
    total_leads = len(leads_db)
    
    # Calculate total opportunities
    total_opportunities = len(opportunities_db)
    
    # Calculate total quotations
    total_quotations = len(quotations_db)
    
    # Calculate conversion rate
    conversion_rate = (deals_closed / total_opportunities * 100) if total_opportunities > 0 else 0
    
    # Create metrics object
    metrics = SalesMetrics(
        total_leads=total_leads,
        total_opportunities=total_opportunities,
        total_quotations=total_quotations,
        total_sales=total_sales,
        deals_closed=deals_closed,
        conversion_rate=conversion_rate
    )
    
    # Group leads by status
    lead_status_counts = {}
    for lead in leads_db:
        status = lead.status
        if status in lead_status_counts:
            lead_status_counts[status] += 1
        else:
            lead_status_counts[status] = 1
    
    leads_by_status = [
        LeadByStatus(status=status, count=count)
        for status, count in lead_status_counts.items()
    ]
    
    # Group opportunities by stage
    opportunity_stage_data = {}
    for opp in opportunities_db:
        stage = opp.stage
        if stage in opportunity_stage_data:
            opportunity_stage_data[stage]["count"] += 1
            opportunity_stage_data[stage]["value"] += opp.amount or 0
        else:
            opportunity_stage_data[stage] = {
                "count": 1,
                "value": opp.amount or 0
            }
    
    opportunities_by_stage = [
        OpportunityByStage(
            stage=stage,
            count=data["count"],
            total_value=data["value"]
        )
        for stage, data in opportunity_stage_data.items()
    ]
    
    # Group quotations by status
    quotation_status_data = {}
    for quote in quotations_db:
        status = quote.status
        if status in quotation_status_data:
            quotation_status_data[status]["count"] += 1
            quotation_status_data[status]["value"] += quote.total
        else:
            quotation_status_data[status] = {
                "count": 1,
                "value": quote.total
            }
    
    quotations_by_status = [
        QuotationByStatus(
            status=status,
            count=data["count"],
            total_value=data["value"]
        )
        for status, data in quotation_status_data.items()
    ]
    
    return SalesReport(
        metrics=metrics,
        leads_by_status=leads_by_status,
        opportunities_by_stage=opportunities_by_stage,
        quotations_by_status=quotations_by_status
    )

@router.get("/reports/sales/metrics", response_model=SalesMetrics)
def sales_metrics():
    # Get the closed won stage from config
    closed_won_stage = get_closed_won_stage()
    
    total_sales = sum([opp.amount or 0 for opp in opportunities_db if opp.stage == closed_won_stage])
    deals_closed = len([opp for opp in opportunities_db if opp.stage == closed_won_stage])
    total_leads = len(leads_db)
    total_opportunities = len(opportunities_db)
    total_quotations = len(quotations_db)
    conversion_rate = (deals_closed / total_opportunities * 100) if total_opportunities > 0 else 0
    
    return SalesMetrics(
        total_leads=total_leads,
        total_opportunities=total_opportunities,
        total_quotations=total_quotations,
        total_sales=total_sales,
        deals_closed=deals_closed,
        conversion_rate=conversion_rate
    )