from fastapi import APIRouter, HTTPException, Depends
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from .models import (
    MarketingMetric, MarketingMetricCreate, MarketingMetricUpdate,
    Report, ReportCreate, ReportUpdate,
    Dashboard, DashboardCreate, DashboardUpdate,
    ConversionTracking, ConversionTrackingCreate, ConversionTrackingUpdate,
    AttributionModel, AttributionModelCreate, AttributionModelUpdate
)
from .config import (
    get_report_types, get_report_frequencies, get_attribution_models,
    get_default_conversion_rate, get_default_customer_lifetime_value
)

router = APIRouter(prefix="/analytics", tags=["analytics"])

# In-memory storage for demo purposes
marketing_metrics_db = []
reports_db = []
dashboards_db = []
conversion_trackings_db = []
attribution_models_db = []

@router.get("/")
def get_analytics_dashboard():
    """Get marketing analytics dashboard with summary statistics"""
    return {
        "message": "Marketing Analytics Dashboard",
        "statistics": {
            "total_metrics": len(marketing_metrics_db),
            "total_reports": len(reports_db),
            "total_dashboards": len(dashboards_db),
            "total_conversion_trackings": len(conversion_trackings_db),
            "total_attribution_models": len(attribution_models_db)
        }
    }

@router.get("/metrics", response_model=List[MarketingMetric])
def list_marketing_metrics():
    """List all marketing metrics"""
    return marketing_metrics_db

@router.get("/metrics/{metric_id}", response_model=MarketingMetric)
def get_marketing_metric(metric_id: int):
    """Get a specific marketing metric by ID"""
    for metric in marketing_metrics_db:
        if metric.id == metric_id:
            return metric
    raise HTTPException(status_code=404, detail="Marketing metric not found")

@router.post("/metrics", response_model=MarketingMetric)
def create_marketing_metric(metric: MarketingMetricCreate):
    """Create a new marketing metric"""
    new_id = max([m.id for m in marketing_metrics_db]) + 1 if marketing_metrics_db else 1
    new_metric = MarketingMetric(
        id=new_id,
        created_at=datetime.now(),
        **metric.dict()
    )
    marketing_metrics_db.append(new_metric)
    return new_metric

@router.put("/metrics/{metric_id}", response_model=MarketingMetric)
def update_marketing_metric(metric_id: int, metric_update: MarketingMetricUpdate):
    """Update an existing marketing metric"""
    for index, metric in enumerate(marketing_metrics_db):
        if metric.id == metric_id:
            updated_metric = MarketingMetric(
                id=metric_id,
                created_at=metric.created_at,
                **metric_update.dict()
            )
            marketing_metrics_db[index] = updated_metric
            return updated_metric
    raise HTTPException(status_code=404, detail="Marketing metric not found")

@router.delete("/metrics/{metric_id}")
def delete_marketing_metric(metric_id: int):
    """Delete a marketing metric"""
    for index, metric in enumerate(marketing_metrics_db):
        if metric.id == metric_id:
            del marketing_metrics_db[index]
            return {"message": "Marketing metric deleted successfully"}
    raise HTTPException(status_code=404, detail="Marketing metric not found")

@router.get("/metrics/campaign/{campaign_id}", response_model=List[MarketingMetric])
def get_metrics_by_campaign(campaign_id: int):
    """Get marketing metrics by campaign ID"""
    return [metric for metric in marketing_metrics_db if metric.campaign_id == campaign_id]

@router.get("/metrics/channel/{channel}", response_model=List[MarketingMetric])
def get_metrics_by_channel(channel: str):
    """Get marketing metrics by channel"""
    return [metric for metric in marketing_metrics_db if metric.channel == channel]

# Reports endpoints
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
                last_generated_at=report.last_generated_at,
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
            report.last_generated_at = datetime.now()
            reports_db[index] = report
            return {"message": f"Report {report_id} generated successfully"}
    raise HTTPException(status_code=404, detail="Report not found")

@router.get("/reports/type/{report_type}", response_model=List[Report])
def get_reports_by_type(report_type: str):
    """Get reports by type"""
    # Normalize the report_type parameter to handle case differences
    normalized_type = report_type.lower().title()
    return [report for report in reports_db if report.report_type == normalized_type]

# Dashboards endpoints
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

# Conversion Tracking endpoints
@router.get("/conversions", response_model=List[ConversionTracking])
def list_conversion_trackings():
    """List all conversion trackings"""
    return conversion_trackings_db

@router.get("/conversions/{conversion_id}", response_model=ConversionTracking)
def get_conversion_tracking(conversion_id: int):
    """Get a specific conversion tracking by ID"""
    for conversion in conversion_trackings_db:
        if conversion.id == conversion_id:
            return conversion
    raise HTTPException(status_code=404, detail="Conversion tracking not found")

@router.post("/conversions", response_model=ConversionTracking)
def create_conversion_tracking(conversion: ConversionTrackingCreate):
    """Create a new conversion tracking"""
    new_id = max([c.id for c in conversion_trackings_db]) + 1 if conversion_trackings_db else 1
    new_conversion = ConversionTracking(
        id=new_id,
        created_at=datetime.now(),
        conversion_count=0,
        conversion_rate=get_default_conversion_rate(),
        **conversion.dict()
    )
    conversion_trackings_db.append(new_conversion)
    return new_conversion

@router.put("/conversions/{conversion_id}", response_model=ConversionTracking)
def update_conversion_tracking(conversion_id: int, conversion_update: ConversionTrackingUpdate):
    """Update an existing conversion tracking"""
    for index, conversion in enumerate(conversion_trackings_db):
        if conversion.id == conversion_id:
            updated_conversion = ConversionTracking(
                id=conversion_id,
                created_at=conversion.created_at,
                updated_at=datetime.now(),
                conversion_count=conversion.conversion_count,
                conversion_rate=conversion.conversion_rate,
                **conversion_update.dict()
            )
            conversion_trackings_db[index] = updated_conversion
            return updated_conversion
    raise HTTPException(status_code=404, detail="Conversion tracking not found")

@router.delete("/conversions/{conversion_id}")
def delete_conversion_tracking(conversion_id: int):
    """Delete a conversion tracking"""
    for index, conversion in enumerate(conversion_trackings_db):
        if conversion.id == conversion_id:
            del conversion_trackings_db[index]
            return {"message": "Conversion tracking deleted successfully"}
    raise HTTPException(status_code=404, detail="Conversion tracking not found")

@router.post("/conversions/{conversion_id}/track")
def track_conversion(conversion_id: int, traffic_count: Optional[int] = None):
    """Track a conversion
    
    Args:
        conversion_id: The ID of the conversion to track
        traffic_count: Optional traffic count for accurate conversion rate calculation
    """
    for index, conversion in enumerate(conversion_trackings_db):
        if conversion.id == conversion_id:
            conversion.conversion_count += 1
            # Calculate conversion rate based on traffic count if provided, otherwise use existing count
            if traffic_count is not None and traffic_count > 0:
                conversion.conversion_rate = conversion.conversion_count / traffic_count
            elif hasattr(conversion, 'traffic_count') and conversion.traffic_count > 0:
                conversion.conversion_rate = conversion.conversion_count / conversion.traffic_count
            else:
                # Fallback to a more realistic calculation based on a default traffic assumption
                # In a real implementation, this would come from actual traffic data
                default_traffic = max(conversion.conversion_count * 10, 100)  # Assume 10x conversions as traffic or minimum 100
                conversion.conversion_rate = conversion.conversion_count / default_traffic
            conversion_trackings_db[index] = conversion
            return {"message": f"Conversion {conversion_id} tracked successfully", 
                    "conversion_rate": conversion.conversion_rate}
    raise HTTPException(status_code=404, detail="Conversion tracking not found")

# Attribution Models endpoints
@router.get("/attribution-models", response_model=List[AttributionModel])
def list_attribution_models():
    """List all attribution models"""
    return attribution_models_db

@router.get("/attribution-models/{model_id}", response_model=AttributionModel)
def get_attribution_model(model_id: int):
    """Get a specific attribution model by ID"""
    for model in attribution_models_db:
        if model.id == model_id:
            return model
    raise HTTPException(status_code=404, detail="Attribution model not found")

@router.post("/attribution-models", response_model=AttributionModel)
def create_attribution_model(model: AttributionModelCreate):
    """Create a new attribution model"""
    new_id = max([m.id for m in attribution_models_db]) + 1 if attribution_models_db else 1
    new_model = AttributionModel(
        id=new_id,
        created_at=datetime.now(),
        **model.dict()
    )
    attribution_models_db.append(new_model)
    return new_model

@router.put("/attribution-models/{model_id}", response_model=AttributionModel)
def update_attribution_model(model_id: int, model_update: AttributionModelUpdate):
    """Update an existing attribution model"""
    for index, model in enumerate(attribution_models_db):
        if model.id == model_id:
            updated_model = AttributionModel(
                id=model_id,
                created_at=model.created_at,
                updated_at=datetime.now(),
                **model_update.dict()
            )
            attribution_models_db[index] = updated_model
            return updated_model
    raise HTTPException(status_code=404, detail="Attribution model not found")

@router.delete("/attribution-models/{model_id}")
def delete_attribution_model(model_id: int):
    """Delete an attribution model"""
    for index, model in enumerate(attribution_models_db):
        if model.id == model_id:
            del attribution_models_db[index]
            return {"message": "Attribution model deleted successfully"}
    raise HTTPException(status_code=404, detail="Attribution model not found")

@router.get("/attribution-models/default", response_model=AttributionModel)
def get_default_attribution_model():
    """Get the default attribution model"""
    for model in attribution_models_db:
        if model.is_default:
            return model
    raise HTTPException(status_code=404, detail="Default attribution model not found")

# Configuration endpoints
@router.get("/config/report-types", response_model=List[str])
def get_report_type_options():
    """Get available report types"""
    return get_report_types()

@router.get("/config/report-frequencies", response_model=List[str])
def get_report_frequency_options():
    """Get available report frequencies"""
    return get_report_frequencies()

@router.get("/config/attribution-models", response_model=List[str])
def get_attribution_model_options():
    """Get available attribution models"""
    return get_attribution_models()