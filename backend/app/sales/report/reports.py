from fastapi import APIRouter
from typing import List, Optional
from datetime import datetime
from .models import Report, ReportCreate, ReportUpdate, ReportType, ReportStatus
from .models import SalesMetrics, LeadByStatus, OpportunityByStage, QuotationByStatus, SalesReport
from ..lead.leads import leads_db
from ..opportunity.opportunities import opportunities_db
from ..quotation.quotations import quotations_db
from .config import get_report_types, get_report_statuses
from ..opportunity.config import get_closed_won_stage

router = APIRouter()

# In-memory storage for demo purposes
reports_db = []

@router.get("/", response_model=List[Report])
def list_reports():
    return reports_db

@router.get("/{report_id}", response_model=Report)
def get_report(report_id: int):
    for report in reports_db:
        if report.id == report_id:
            return report
    return None

@router.post("/", response_model=Report)
def create_report(report: ReportCreate):
    new_id = max([r.id for r in reports_db]) + 1 if reports_db else 1
    new_report = Report(
        id=new_id,
        created_at=datetime.now(),
        **report.dict()
    )
    reports_db.append(new_report)
    return new_report

@router.put("/{report_id}", response_model=Report)
def update_report(report_id: int, report_update: ReportUpdate):
    for index, report in enumerate(reports_db):
        if report.id == report_id:
            updated_report = Report(
                id=report_id,
                created_at=report.created_at,
                updated_at=datetime.now(),
                **report_update.dict()
            )
            reports_db[index] = updated_report
            return updated_report
    return None

@router.delete("/{report_id}")
def delete_report(report_id: int):
    for index, report in enumerate(reports_db):
        if report.id == report_id:
            del reports_db[index]
            return {"message": "Report deleted successfully"}
    return {"message": "Report not found"}

@router.get("/sales", response_model=SalesReport)
def sales_report():
    # Get the closed won stage from config
    closed_won_stage = get_closed_won_stage()
    
    # Calculate total sales and deals closed
    total_sales = sum([opp.value or 0 for opp in opportunities_db if opp.stage.value == closed_won_stage])
    deals_closed = len([opp for opp in opportunities_db if opp.stage.value == closed_won_stage])
    
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
        status = lead.status.value
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
        stage = opp.stage.value
        if stage in opportunity_stage_data:
            opportunity_stage_data[stage]["count"] += 1
            opportunity_stage_data[stage]["value"] += opp.value or 0
        else:
            opportunity_stage_data[stage] = {
                "count": 1,
                "value": opp.value or 0
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
        status = quote.status.value
        if status in quotation_status_data:
            quotation_status_data[status]["count"] += 1
            quotation_status_data[status]["value"] += quote.total_amount
        else:
            quotation_status_data[status] = {
                "count": 1,
                "value": quote.total_amount
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

@router.get("/sales/metrics", response_model=SalesMetrics)
def sales_metrics():
    # Get the closed won stage from config
    closed_won_stage = get_closed_won_stage()
    
    total_sales = sum([opp.value or 0 for opp in opportunities_db if opp.stage.value == closed_won_stage])
    deals_closed = len([opp for opp in opportunities_db if opp.stage.value == closed_won_stage])
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

@router.get("/config/types", response_model=List[str])
def get_report_type_options():
    """Get available report types"""
    return get_report_types()

@router.get("/config/statuses", response_model=List[str])
def get_report_status_options():
    """Get available report statuses"""
    return get_report_statuses()