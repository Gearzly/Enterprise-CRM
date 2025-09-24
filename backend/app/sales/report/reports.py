from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from .models import Report, ReportCreate, ReportUpdate
from .models import SalesMetrics, LeadByStatus, OpportunityByStage, QuotationByStatus, SalesReport
from .config import get_report_types, get_report_statuses
from app.core.deps import get_db
from app.core.crud import report as crud_report
# Import CRUD modules for related entities
from app.core.crud import lead as crud_lead
from app.core.crud import opportunity as crud_opportunity
from app.core.crud import quotation as crud_quotation
# Import config functions
from ..opportunity.config import get_closed_won_stage

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/")
def get_reports_dashboard():
    """Get sales reports dashboard with summary statistics"""
    return {
        "message": "Sales Reports Dashboard",
        "statistics": {
            "total_reports": "Available via list endpoint",
            "sales_metrics": "Available via sales/metrics endpoint",
            "sales_report": "Available via sales endpoint",
            "leads_by_status": "Included in sales report"
        }
    }

@router.get("/reports", response_model=List[Report])
def list_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all reports"""
    reports = crud_report.get_multi(db, skip=skip, limit=limit)
    return reports

@router.get("/{report_id}", response_model=Report)
def get_report(report_id: int, db: Session = Depends(get_db)):
    """Get a specific report by ID"""
    db_report = crud_report.get(db, id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return db_report

@router.post("/", response_model=Report)
def create_report(report: ReportCreate, db: Session = Depends(get_db)):
    """Create a new report"""
    return crud_report.create(db, obj_in=report)

@router.put("/{report_id}", response_model=Report)
def update_report(report_id: int, report_update: ReportUpdate, db: Session = Depends(get_db)):
    """Update an existing report"""
    db_report = crud_report.get(db, id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return crud_report.update(db, db_obj=db_report, obj_in=report_update)

@router.delete("/{report_id}")
def delete_report(report_id: int, db: Session = Depends(get_db)):
    """Delete a report"""
    db_report = crud_report.get(db, id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    crud_report.remove(db, id=report_id)
    return {"message": "Report deleted successfully"}

@router.get("/sales", response_model=SalesReport)
def sales_report(db: Session = Depends(get_db)):
    """Generate a sales report with metrics and breakdowns"""
    # Get the closed won stage from config
    closed_won_stage = get_closed_won_stage()
    
    # Get all related data from database
    leads = crud_lead.get_multi(db)
    opportunities = crud_opportunity.get_multi(db)
    quotations = crud_quotation.get_multi(db)
    
    # Calculate total sales and deals closed
    total_sales = 0.0
    deals_closed = 0
    for opp in opportunities:
        # Access the actual value of the stage attribute
        stage_value = str(opp.stage)
        if stage_value == closed_won_stage:
            # Access the actual value of the value attribute
            opp_value = opp.value if opp.value is not None else 0.0
            total_sales += opp_value
            deals_closed += 1
    
    # Calculate total leads
    total_leads = len(leads)
    
    # Calculate total opportunities
    total_opportunities = len(opportunities)
    
    # Calculate total quotations
    total_quotations = len(quotations)
    
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
    for lead in leads:
        status = str(lead.status)
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
    for opp in opportunities:
        stage = str(opp.stage)
        opp_value = opp.value if opp.value is not None else 0.0
        if stage in opportunity_stage_data:
            opportunity_stage_data[stage]["count"] += 1
            opportunity_stage_data[stage]["value"] += opp_value
        else:
            opportunity_stage_data[stage] = {
                "count": 1,
                "value": opp_value
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
    for quote in quotations:
        status = str(quote.status)
        quote_total = quote.total_amount if quote.total_amount is not None else 0.0
        if status in quotation_status_data:
            quotation_status_data[status]["count"] += 1
            quotation_status_data[status]["value"] += quote_total
        else:
            quotation_status_data[status] = {
                "count": 1,
                "value": quote_total
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
def sales_metrics(db: Session = Depends(get_db)):
    """Get sales metrics only"""
    # Get the closed won stage from config
    closed_won_stage = get_closed_won_stage()
    
    # Get all related data from database
    leads = crud_lead.get_multi(db)
    opportunities = crud_opportunity.get_multi(db)
    quotations = crud_quotation.get_multi(db)
    
    total_sales = 0.0
    deals_closed = 0
    for opp in opportunities:
        # Access the actual value of the stage attribute
        stage_value = str(opp.stage)
        if stage_value == closed_won_stage:
            # Access the actual value of the value attribute
            opp_value = opp.value if opp.value is not None else 0.0
            total_sales += opp_value
            deals_closed += 1
    
    total_leads = len(leads)
    total_opportunities = len(opportunities)
    total_quotations = len(quotations)
    conversion_rate = (deals_closed / total_opportunities * 100) if total_opportunities > 0 else 0
    
    return SalesMetrics(
        total_leads=total_leads,
        total_opportunities=total_opportunities,
        total_quotations=total_quotations,
        total_sales=total_sales,
        deals_closed=deals_closed,
        conversion_rate=conversion_rate
    )

@router.get("/type/{report_type}", response_model=List[Report])
def get_reports_by_type(report_type: str, db: Session = Depends(get_db)):
    """Get reports by type"""
    return crud_report.get_by_type(db, report_type=report_type)

@router.get("/status/{status}", response_model=List[Report])
def get_reports_by_status(status: str, db: Session = Depends(get_db)):
    """Get reports by status"""
    return crud_report.get_by_status(db, status=status)

@router.get("/generated-by/{generated_by}", response_model=List[Report])
def get_reports_by_generated_by(generated_by: str, db: Session = Depends(get_db)):
    """Get reports by generated by"""
    return crud_report.get_by_generated_by(db, generated_by=generated_by)

@router.get("/recent/{days}", response_model=List[Report])
def get_recent_reports(days: int, db: Session = Depends(get_db)):
    """Get reports generated in the last N days"""
    cutoff_date = datetime.now() - timedelta(days=days)
    from sqlalchemy import and_
    return db.query(crud_report.model).filter(crud_report.model.created_at >= cutoff_date).all()

@router.get("/config/types", response_model=List[str])
def get_report_type_options():
    """Get available report types"""
    return get_report_types()

@router.get("/config/statuses", response_model=List[str])
def get_report_status_options():
    """Get available report statuses"""
    return get_report_statuses()