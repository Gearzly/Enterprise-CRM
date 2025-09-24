from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from .models import (
    Report, ReportCreate, ReportUpdate,
    ReportDataPoint, ReportDataPointCreate,
    Dashboard, DashboardCreate, DashboardUpdate,
    DashboardWidget, DashboardWidgetCreate, DashboardWidgetUpdate,
    Metric, MetricCreate, MetricUpdate
)
from .config import (
    get_report_types, get_report_frequencies, get_report_statuses,
    get_default_report_frequency, get_default_report_type, get_max_data_points_per_report
)

router = APIRouter(prefix="/reporting", tags=["reporting"])

# In-memory storage for demo purposes
reports_db = []
report_data_points_db = []
dashboards_db = []
dashboard_widgets_db = []
metrics_db = []

@router.get("/")
def get_reporting_dashboard():
    """Get support reporting dashboard with summary statistics"""
    return {
        "message": "Support Reporting Dashboard",
        "statistics": {
            "total_reports": len(reports_db),
            "dashboards": len(dashboards_db),
            "active_metrics": len([m for m in metrics_db if m.is_active]),
            "widgets": len(dashboard_widgets_db)
        }
    }

@router.get("/reports", response_model=List[Report])
def list_reports():
    """List all reports"""
    return reports_db

@router.get("/reports/{report_id}", response_model=Report)
def get_report(report_id: int):
    """Get a specific report by ID"""
    for report in reports_db:
        if report.id == report_id:
            return report
    raise HTTPException(status_code=404, detail="Report not found")

@router.post("/reports", response_model=Report)
def create_report(report: ReportCreate):
    """Create a new report"""
    new_id = max([r.id for r in reports_db]) + 1 if reports_db else 1
    new_report = Report(
        id=new_id,
        created_at=datetime.now(),
        **report.dict()
    )
    reports_db.append(new_report)
    return new_report

@router.put("/reports/{report_id}", response_model=Report)
def update_report(report_id: int, report_update: ReportUpdate):
    """Update an existing report"""
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
    raise HTTPException(status_code=404, detail="Report not found")

@router.delete("/reports/{report_id}")
def delete_report(report_id: int):
    """Delete a report"""
    for index, report in enumerate(reports_db):
        if report.id == report_id:
            del reports_db[index]
            return {"message": "Report deleted successfully"}
    raise HTTPException(status_code=404, detail="Report not found")

@router.post("/reports/{report_id}/generate")
def generate_report(report_id: int):
    """Generate a report"""
    for index, report in enumerate(reports_db):
        if report.id == report_id:
            reports_db[index].status = "Generating"
            # In a real implementation, this would trigger the actual report generation process
            reports_db[index].status = "Completed"
            reports_db[index].last_generated_at = datetime.now()
            return {"message": "Report generation completed successfully"}
    raise HTTPException(status_code=404, detail="Report not found")

@router.post("/reports/{report_id}/schedule")
def schedule_report(report_id: int):
    """Schedule a report"""
    for index, report in enumerate(reports_db):
        if report.id == report_id:
            # In a real implementation, this would set up a scheduled task
            return {"message": "Report scheduled successfully"}
    raise HTTPException(status_code=404, detail="Report not found")

@router.get("/reports/type/{type}", response_model=List[Report])
def get_reports_by_type(type: str):
    """Get reports by type"""
    # Normalize the type parameter to handle case differences
    normalized_type = type.lower().title()
    return [report for report in reports_db if report.type == normalized_type]

@router.get("/reports/frequency/{frequency}", response_model=List[Report])
def get_reports_by_frequency(frequency: str):
    """Get reports by frequency"""
    # Normalize the frequency parameter to handle case differences
    normalized_frequency = frequency.lower().title()
    return [report for report in reports_db if report.frequency == normalized_frequency]

@router.get("/reports/status/{status}", response_model=List[Report])
def get_reports_by_status(status: str):
    """Get reports by status"""
    # Normalize the status parameter to handle case differences
    normalized_status = status.lower().title()
    return [report for report in reports_db if report.status == normalized_status]

# Report Data Point endpoints
@router.get("/data-points", response_model=List[ReportDataPoint])
def list_report_data_points():
    """List all report data points"""
    return report_data_points_db

@router.get("/data-points/{data_point_id}", response_model=ReportDataPoint)
def get_report_data_point(data_point_id: int):
    """Get a specific report data point by ID"""
    for data_point in report_data_points_db:
        if data_point.id == data_point_id:
            return data_point
    raise HTTPException(status_code=404, detail="Report data point not found")

@router.post("/data-points", response_model=ReportDataPoint)
def create_report_data_point(data_point: ReportDataPointCreate):
    """Create a new report data point"""
    new_id = max([d.id for d in report_data_points_db]) + 1 if report_data_points_db else 1
    new_data_point = ReportDataPoint(
        id=new_id,
        **data_point.dict()
    )
    report_data_points_db.append(new_data_point)
    return new_data_point

@router.get("/reports/{report_id}/data-points", response_model=List[ReportDataPoint])
def get_data_points_for_report(report_id: int):
    """Get data points for a specific report"""
    return [data_point for data_point in report_data_points_db if data_point.report_id == report_id]

# Dashboard endpoints
@router.get("/dashboards", response_model=List[Dashboard])
def list_dashboards():
    """List all dashboards"""
    return dashboards_db

@router.get("/dashboards/{dashboard_id}", response_model=Dashboard)
def get_dashboard(dashboard_id: int):
    """Get a specific dashboard by ID"""
    for dashboard in dashboards_db:
        if dashboard.id == dashboard_id:
            return dashboard
    raise HTTPException(status_code=404, detail="Dashboard not found")

@router.post("/dashboards", response_model=Dashboard)
def create_dashboard(dashboard: DashboardCreate):
    """Create a new dashboard"""
    new_id = max([d.id for d in dashboards_db]) + 1 if dashboards_db else 1
    new_dashboard = Dashboard(
        id=new_id,
        created_at=datetime.now(),
        **dashboard.dict()
    )
    dashboards_db.append(new_dashboard)
    return new_dashboard

@router.put("/dashboards/{dashboard_id}", response_model=Dashboard)
def update_dashboard(dashboard_id: int, dashboard_update: DashboardUpdate):
    """Update an existing dashboard"""
    for index, dashboard in enumerate(dashboards_db):
        if dashboard.id == dashboard_id:
            updated_dashboard = Dashboard(
                id=dashboard_id,
                created_at=dashboard.created_at,
                updated_at=datetime.now(),
                **dashboard_update.dict()
            )
            dashboards_db[index] = updated_dashboard
            return updated_dashboard
    raise HTTPException(status_code=404, detail="Dashboard not found")

@router.delete("/dashboards/{dashboard_id}")
def delete_dashboard(dashboard_id: int):
    """Delete a dashboard"""
    for index, dashboard in enumerate(dashboards_db):
        if dashboard.id == dashboard_id:
            del dashboards_db[index]
            return {"message": "Dashboard deleted successfully"}
    raise HTTPException(status_code=404, detail="Dashboard not found")

@router.post("/dashboards/{dashboard_id}/share")
def share_dashboard(dashboard_id: int):
    """Share a dashboard"""
    for index, dashboard in enumerate(dashboards_db):
        if dashboard.id == dashboard_id:
            dashboards_db[index].is_public = True
            return {"message": "Dashboard shared successfully"}
    raise HTTPException(status_code=404, detail="Dashboard not found")

# Dashboard Widget endpoints
@router.get("/widgets", response_model=List[DashboardWidget])
def list_dashboard_widgets():
    """List all dashboard widgets"""
    return dashboard_widgets_db

@router.get("/widgets/{widget_id}", response_model=DashboardWidget)
def get_dashboard_widget(widget_id: int):
    """Get a specific dashboard widget by ID"""
    for widget in dashboard_widgets_db:
        if widget.id == widget_id:
            return widget
    raise HTTPException(status_code=404, detail="Dashboard widget not found")

@router.post("/widgets", response_model=DashboardWidget)
def create_dashboard_widget(widget: DashboardWidgetCreate):
    """Create a new dashboard widget"""
    new_id = max([w.id for w in dashboard_widgets_db]) + 1 if dashboard_widgets_db else 1
    new_widget = DashboardWidget(
        id=new_id,
        created_at=datetime.now(),
        **widget.dict()
    )
    dashboard_widgets_db.append(new_widget)
    return new_widget

@router.put("/widgets/{widget_id}", response_model=DashboardWidget)
def update_dashboard_widget(widget_id: int, widget_update: DashboardWidgetUpdate):
    """Update an existing dashboard widget"""
    for index, widget in enumerate(dashboard_widgets_db):
        if widget.id == widget_id:
            updated_widget = DashboardWidget(
                id=widget_id,
                created_at=widget.created_at,
                updated_at=datetime.now(),
                **widget_update.dict()
            )
            dashboard_widgets_db[index] = updated_widget
            return updated_widget
    raise HTTPException(status_code=404, detail="Dashboard widget not found")

@router.delete("/widgets/{widget_id}")
def delete_dashboard_widget(widget_id: int):
    """Delete a dashboard widget"""
    for index, widget in enumerate(dashboard_widgets_db):
        if widget.id == widget_id:
            del dashboard_widgets_db[index]
            return {"message": "Dashboard widget deleted successfully"}
    raise HTTPException(status_code=404, detail="Dashboard widget not found")

@router.get("/dashboards/{dashboard_id}/widgets", response_model=List[DashboardWidget])
def get_widgets_for_dashboard(dashboard_id: int):
    """Get widgets for a specific dashboard"""
    return [widget for widget in dashboard_widgets_db if widget.dashboard_id == dashboard_id]

# Metric endpoints
@router.get("/metrics", response_model=List[Metric])
def list_metrics():
    """List all metrics"""
    return metrics_db

@router.get("/metrics/{metric_id}", response_model=Metric)
def get_metric(metric_id: int):
    """Get a specific metric by ID"""
    for metric in metrics_db:
        if metric.id == metric_id:
            return metric
    raise HTTPException(status_code=404, detail="Metric not found")

@router.post("/metrics", response_model=Metric)
def create_metric(metric: MetricCreate):
    """Create a new metric"""
    new_id = max([m.id for m in metrics_db]) + 1 if metrics_db else 1
    new_metric = Metric(
        id=new_id,
        created_at=datetime.now(),
        **metric.dict()
    )
    metrics_db.append(new_metric)
    return new_metric

@router.put("/metrics/{metric_id}", response_model=Metric)
def update_metric(metric_id: int, metric_update: MetricUpdate):
    """Update an existing metric"""
    for index, metric in enumerate(metrics_db):
        if metric.id == metric_id:
            updated_metric = Metric(
                id=metric_id,
                created_at=metric.created_at,
                updated_at=datetime.now(),
                **metric_update.dict()
            )
            metrics_db[index] = updated_metric
            return updated_metric
    raise HTTPException(status_code=404, detail="Metric not found")

@router.delete("/metrics/{metric_id}")
def delete_metric(metric_id: int):
    """Delete a metric"""
    for index, metric in enumerate(metrics_db):
        if metric.id == metric_id:
            del metrics_db[index]
            return {"message": "Metric deleted successfully"}
    raise HTTPException(status_code=404, detail="Metric not found")

@router.post("/metrics/{metric_id}/activate")
def activate_metric(metric_id: int):
    """Activate a metric"""
    for index, metric in enumerate(metrics_db):
        if metric.id == metric_id:
            metrics_db[index].is_active = True
            return {"message": "Metric activated successfully"}
    raise HTTPException(status_code=404, detail="Metric not found")

@router.post("/metrics/{metric_id}/deactivate")
def deactivate_metric(metric_id: int):
    """Deactivate a metric"""
    for index, metric in enumerate(metrics_db):
        if metric.id == metric_id:
            metrics_db[index].is_active = False
            return {"message": "Metric deactivated successfully"}
    raise HTTPException(status_code=404, detail="Metric not found")

@router.get("/metrics/category/{category}", response_model=List[Metric])
def get_metrics_by_category(category: str):
    """Get metrics by category"""
    return [metric for metric in metrics_db if metric.category == category]

# Configuration endpoints
@router.get("/config/report-types", response_model=List[str])
def get_report_type_options():
    """Get available report type options"""
    return get_report_types()

@router.get("/config/frequencies", response_model=List[str])
def get_report_frequency_options():
    """Get available report frequency options"""
    return get_report_frequencies()

@router.get("/config/statuses", response_model=List[str])
def get_report_status_options():
    """Get available report status options"""
    return get_report_statuses()