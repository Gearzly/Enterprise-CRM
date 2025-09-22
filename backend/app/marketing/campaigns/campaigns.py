from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum
from .models import (
    Campaign, CampaignCreate, CampaignUpdate,
    CampaignTemplate, CampaignTemplateCreate, CampaignTemplateUpdate,
    ABTest, ABTestCreate, ABTestUpdate
)
from .config import (
    get_campaign_statuses, get_campaign_types, 
    get_ab_test_metrics, get_default_budget
)

router = APIRouter()

# In-memory storage for demo purposes
campaigns_db = []
campaign_templates_db = []
ab_tests_db = []

@router.get("/", response_model=List[Campaign])
def list_campaigns():
    """List all campaigns"""
    return campaigns_db

@router.get("/{campaign_id}", response_model=Campaign)
def get_campaign(campaign_id: int):
    """Get a specific campaign by ID"""
    for campaign in campaigns_db:
        if campaign.id == campaign_id:
            return campaign
    raise HTTPException(status_code=404, detail="Campaign not found")

@router.post("/", response_model=Campaign)
def create_campaign(campaign: CampaignCreate):
    """Create a new campaign"""
    new_id = max([c.id for c in campaigns_db]) + 1 if campaigns_db else 1
    new_campaign = Campaign(
        id=new_id,
        created_at=datetime.now(),
        **campaign.dict()
    )
    campaigns_db.append(new_campaign)
    return new_campaign

@router.put("/{campaign_id}", response_model=Campaign)
def update_campaign(campaign_id: int, campaign_update: CampaignUpdate):
    """Update an existing campaign"""
    for index, campaign in enumerate(campaigns_db):
        if campaign.id == campaign_id:
            updated_campaign = Campaign(
                id=campaign_id,
                created_at=campaign.created_at,
                updated_at=datetime.now(),
                **campaign_update.dict()
            )
            campaigns_db[index] = updated_campaign
            return updated_campaign
    raise HTTPException(status_code=404, detail="Campaign not found")

@router.delete("/{campaign_id}")
def delete_campaign(campaign_id: int):
    """Delete a campaign"""
    for index, campaign in enumerate(campaigns_db):
        if campaign.id == campaign_id:
            del campaigns_db[index]
            return {"message": "Campaign deleted successfully"}
    raise HTTPException(status_code=404, detail="Campaign not found")

@router.get("/status/{status}", response_model=List[Campaign])
def get_campaigns_by_status(status: str):
    """Get campaigns by status"""
    # Normalize the status parameter to handle case differences
    normalized_status = status.lower().title()
    return [campaign for campaign in campaigns_db if campaign.status.value == normalized_status]

@router.get("/type/{type}", response_model=List[Campaign])
def get_campaigns_by_type(type: str):
    """Get campaigns by type"""
    # Normalize the type parameter to handle case differences
    normalized_type = type.lower().title()
    return [campaign for campaign in campaigns_db if campaign.type.value == normalized_type]

# Campaign Templates endpoints
@router.get("/templates", response_model=List[CampaignTemplate])
def list_campaign_templates():
    """List all campaign templates"""
    return campaign_templates_db

@router.get("/templates/{template_id}", response_model=CampaignTemplate)
def get_campaign_template(template_id: int):
    """Get a specific campaign template by ID"""
    for template in campaign_templates_db:
        if template.id == template_id:
            return template
    raise HTTPException(status_code=404, detail="Campaign template not found")

@router.post("/templates", response_model=CampaignTemplate)
def create_campaign_template(template: CampaignTemplateCreate):
    """Create a new campaign template"""
    new_id = max([t.id for t in campaign_templates_db]) + 1 if campaign_templates_db else 1
    new_template = CampaignTemplate(
        id=new_id,
        created_at=datetime.now(),
        **template.dict()
    )
    campaign_templates_db.append(new_template)
    return new_template

@router.put("/templates/{template_id}", response_model=CampaignTemplate)
def update_campaign_template(template_id: int, template_update: CampaignTemplateUpdate):
    """Update an existing campaign template"""
    for index, template in enumerate(campaign_templates_db):
        if template.id == template_id:
            updated_template = CampaignTemplate(
                id=template_id,
                created_at=template.created_at,
                updated_at=datetime.now(),
                **template_update.dict()
            )
            campaign_templates_db[index] = updated_template
            return updated_template
    raise HTTPException(status_code=404, detail="Campaign template not found")

@router.delete("/templates/{template_id}")
def delete_campaign_template(template_id: int):
    """Delete a campaign template"""
    for index, template in enumerate(campaign_templates_db):
        if template.id == template_id:
            del campaign_templates_db[index]
            return {"message": "Campaign template deleted successfully"}
    raise HTTPException(status_code=404, detail="Campaign template not found")

# A/B Testing endpoints
@router.get("/ab-tests", response_model=List[ABTest])
def list_ab_tests():
    """List all A/B tests"""
    return ab_tests_db

@router.get("/ab-tests/{test_id}", response_model=ABTest)
def get_ab_test(test_id: int):
    """Get a specific A/B test by ID"""
    for test in ab_tests_db:
        if test.id == test_id:
            return test
    raise HTTPException(status_code=404, detail="A/B test not found")

@router.post("/ab-tests", response_model=ABTest)
def create_ab_test(test: ABTestCreate):
    """Create a new A/B test"""
    new_id = max([t.id for t in ab_tests_db]) + 1 if ab_tests_db else 1
    new_test = ABTest(
        id=new_id,
        created_at=datetime.now(),
        **test.dict()
    )
    ab_tests_db.append(new_test)
    return new_test

@router.put("/ab-tests/{test_id}", response_model=ABTest)
def update_ab_test(test_id: int, test_update: ABTestUpdate):
    """Update an existing A/B test"""
    for index, test in enumerate(ab_tests_db):
        if test.id == test_id:
            updated_test = ABTest(
                id=test_id,
                created_at=test.created_at,
                updated_at=datetime.now(),
                **test_update.dict()
            )
            ab_tests_db[index] = updated_test
            return updated_test
    raise HTTPException(status_code=404, detail="A/B test not found")

@router.delete("/ab-tests/{test_id}")
def delete_ab_test(test_id: int):
    """Delete an A/B test"""
    for index, test in enumerate(ab_tests_db):
        if test.id == test_id:
            del ab_tests_db[index]
            return {"message": "A/B test deleted successfully"}
    raise HTTPException(status_code=404, detail="A/B test not found")

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