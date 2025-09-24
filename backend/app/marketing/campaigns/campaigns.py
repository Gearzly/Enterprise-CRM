from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from .models import (
    Campaign, CampaignCreate, CampaignUpdate,
    CampaignTemplate, CampaignTemplateCreate, CampaignTemplateUpdate,
    ABTest, ABTestCreate, ABTestUpdate
)
from .config import (
    get_campaign_statuses, get_campaign_types, 
    get_ab_test_metrics, get_default_budget
)
from .service import CampaignService, CampaignTemplateService, ABTestService
from app.core.database import get_db

router = APIRouter(prefix="/campaigns", tags=["campaigns"])

# Initialize services
campaign_service = CampaignService()
template_service = CampaignTemplateService()
ab_test_service = ABTestService()

@router.get("/")
def get_campaigns_dashboard():
    """Get marketing campaigns dashboard with summary statistics"""
    return {
        "message": "Marketing Campaigns Dashboard",
        "statistics": {
            "total_campaigns": "Available via list endpoint",
            "active_campaigns": "Filtered by status",
            "campaign_templates": "Available via templates endpoint",
            "ab_tests": "Available via ab-tests endpoint"
        }
    }

@router.get("/", response_model=List[Campaign])
def list_campaigns(db: Session = Depends(get_db)):
    """List all campaigns"""
    return campaign_service.get_campaigns(db)

@router.get("/{campaign_id}", response_model=Campaign)
def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    """Get a specific campaign by ID"""
    campaign = campaign_service.get_campaign(db, campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@router.post("/", response_model=Campaign)
def create_campaign(campaign: CampaignCreate, db: Session = Depends(get_db)):
    """Create a new campaign"""
    return campaign_service.create_campaign(db, campaign)

@router.put("/{campaign_id}", response_model=Campaign)
def update_campaign(campaign_id: int, campaign_update: CampaignUpdate, db: Session = Depends(get_db)):
    """Update an existing campaign"""
    campaign = campaign_service.update_campaign(db, campaign_id, campaign_update)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@router.delete("/{campaign_id}")
def delete_campaign(campaign_id: int, db: Session = Depends(get_db)):
    """Delete a campaign"""
    success = campaign_service.delete_campaign(db, campaign_id)
    if not success:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return {"message": "Campaign deleted successfully"}

@router.get("/status/{status}", response_model=List[Campaign])
def get_campaigns_by_status(status: str, db: Session = Depends(get_db)):
    """Get campaigns by status"""
    return campaign_service.get_campaigns_by_status(db, status)

@router.get("/type/{type}", response_model=List[Campaign])
def get_campaigns_by_type(type: str, db: Session = Depends(get_db)):
    """Get campaigns by type"""
    return campaign_service.get_campaigns_by_type(db, type)

# Campaign Templates endpoints
@router.get("/templates", response_model=List[CampaignTemplate])
def list_campaign_templates(db: Session = Depends(get_db)):
    """List all campaign templates"""
    return template_service.get_templates(db)

@router.get("/templates/{template_id}", response_model=CampaignTemplate)
def get_campaign_template(template_id: int, db: Session = Depends(get_db)):
    """Get a specific campaign template by ID"""
    template = template_service.get_template(db, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Campaign template not found")
    return template

@router.post("/templates", response_model=CampaignTemplate)
def create_campaign_template(template: CampaignTemplateCreate, db: Session = Depends(get_db)):
    """Create a new campaign template"""
    return template_service.create_template(db, template)

@router.put("/templates/{template_id}", response_model=CampaignTemplate)
def update_campaign_template(template_id: int, template_update: CampaignTemplateUpdate, db: Session = Depends(get_db)):
    """Update an existing campaign template"""
    template = template_service.update_template(db, template_id, template_update)
    if not template:
        raise HTTPException(status_code=404, detail="Campaign template not found")
    return template

@router.delete("/templates/{template_id}")
def delete_campaign_template(template_id: int, db: Session = Depends(get_db)):
    """Delete a campaign template"""
    success = template_service.delete_template(db, template_id)
    if not success:
        raise HTTPException(status_code=404, detail="Campaign template not found")
    return {"message": "Campaign template deleted successfully"}

# A/B Testing endpoints
@router.get("/ab-tests", response_model=List[ABTest])
def list_ab_tests(db: Session = Depends(get_db)):
    """List all A/B tests"""
    return ab_test_service.get_ab_tests(db)

@router.get("/ab-tests/{test_id}", response_model=ABTest)
def get_ab_test(test_id: int, db: Session = Depends(get_db)):
    """Get a specific A/B test by ID"""
    test = ab_test_service.get_ab_test(db, test_id)
    if not test:
        raise HTTPException(status_code=404, detail="A/B test not found")
    return test

@router.post("/ab-tests", response_model=ABTest)
def create_ab_test(test: ABTestCreate, db: Session = Depends(get_db)):
    """Create a new A/B test"""
    return ab_test_service.create_ab_test(db, test)

@router.put("/ab-tests/{test_id}", response_model=ABTest)
def update_ab_test(test_id: int, test_update: ABTestUpdate, db: Session = Depends(get_db)):
    """Update an existing A/B test"""
    test = ab_test_service.update_ab_test(db, test_id, test_update)
    if not test:
        raise HTTPException(status_code=404, detail="A/B test not found")
    return test

@router.delete("/ab-tests/{test_id}")
def delete_ab_test(test_id: int, db: Session = Depends(get_db)):
    """Delete an A/B test"""
    success = ab_test_service.delete_ab_test(db, test_id)
    if not success:
        raise HTTPException(status_code=404, detail="A/B test not found")
    return {"message": "A/B test deleted successfully"}

# Configuration endpoints
@router.get("/config/statuses", response_model=List[str])
def get_campaign_status_options():
    """Get available campaign status options"""
    return get_campaign_statuses()

@router.get("/config/types", response_model=List[str])
def get_campaign_type_options():
    """Get available campaign type options"""
    return get_campaign_types()

@router.get("/config/ab-test-metrics", response_model=List[str])
def get_ab_test_metric_options():
    """Get available A/B test metrics"""
    return get_ab_test_metrics()