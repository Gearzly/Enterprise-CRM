from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime
from .models import MarketingConfig, MarketingConfigCreate, MarketingConfigUpdate

router = APIRouter()

# In-memory storage for demo purposes
marketing_config_db = [
    # Campaign Management Configs
    MarketingConfig(
        id=1,
        key="campaign_statuses",
        value='["Draft", "Scheduled", "Active", "Paused", "Completed", "Cancelled"]',
        description="Available campaign statuses",
        category="campaigns",
        organization_id=None,
        created_at=datetime.now()
    ),
    MarketingConfig(
        id=2,
        key="campaign_types",
        value='["Email", "Social Media", "Direct Mail", "PPC", "Content", "Event", "Other"]',
        description="Available campaign types",
        category="campaigns",
        organization_id=None,
        created_at=datetime.now()
    ),
    MarketingConfig(
        id=3,
        key="ab_test_metrics",
        value='["click_rate", "conversion_rate", "open_rate", "bounce_rate"]',
        description="Available A/B test metrics",
        category="campaigns",
        organization_id=None,
        created_at=datetime.now()
    ),
    
    # Lead Management Configs
    MarketingConfig(
        id=4,
        key="lead_statuses",
        value='["New", "Contacted", "Nurtured", "Qualified", "Unqualified", "Converted"]',
        description="Available lead statuses",
        category="leads",
        organization_id=None,
        created_at=datetime.now()
    ),
    MarketingConfig(
        id=5,
        key="lead_sources",
        value='["Website", "Referral", "Social Media", "Email Campaign", "Event", "Partner", "Other"]',
        description="Available lead sources",
        category="leads",
        organization_id=None,
        created_at=datetime.now()
    ),
    MarketingConfig(
        id=6,
        key="lead_score_rule_types",
        value='["Demographic", "Behavioral", "Engagement", "Firmographic"]',
        description="Available lead score rule types",
        category="leads",
        organization_id=None,
        created_at=datetime.now()
    ),
    
    # Email Marketing Configs
    MarketingConfig(
        id=7,
        key="email_statuses",
        value='["Draft", "Scheduled", "Sending", "Sent", "Failed"]',
        description="Available email statuses",
        category="email",
        organization_id=None,
        created_at=datetime.now()
    ),
    MarketingConfig(
        id=8,
        key="email_template_categories",
        value='["Newsletter", "Promotional", "Transactional", "Welcome", "Abandoned Cart", "Other"]',
        description="Available email template categories",
        category="email",
        organization_id=None,
        created_at=datetime.now()
    ),
    
    # Social Media Configs
    MarketingConfig(
        id=9,
        key="social_platforms",
        value='["Facebook", "Twitter", "LinkedIn", "Instagram", "YouTube", "TikTok", "Pinterest", "Other"]',
        description="Available social platforms",
        category="social_media",
        organization_id=None,
        created_at=datetime.now()
    ),
    MarketingConfig(
        id=10,
        key="post_statuses",
        value='["Draft", "Scheduled", "Published", "Failed"]',
        description="Available post statuses",
        category="social_media",
        organization_id=None,
        created_at=datetime.now()
    ),
    
    # Content Management Configs
    MarketingConfig(
        id=11,
        key="content_statuses",
        value='["Draft", "Review", "Approved", "Published", "Archived"]',
        description="Available content statuses",
        category="content",
        organization_id=None,
        created_at=datetime.now()
    ),
    MarketingConfig(
        id=12,
        key="content_types",
        value='["Blog Post", "Video", "Image", "Infographic", "eBook", "Whitepaper", "Case Study", "Webinar", "Podcast", "Other"]',
        description="Available content types",
        category="content",
        organization_id=None,
        created_at=datetime.now()
    ),
    
    # Analytics Configs
    MarketingConfig(
        id=13,
        key="report_types",
        value='["Campaign Performance", "Lead Generation", "Email Marketing", "Social Media", "Content Performance", "ROI Dashboard", "Conversion Tracking", "Attribution Modeling", "Customer Lifetime Value", "Channel Performance"]',
        description="Available report types",
        category="analytics",
        organization_id=None,
        created_at=datetime.now()
    ),
    MarketingConfig(
        id=14,
        key="attribution_models",
        value='["First Touch", "Last Touch", "Linear", "Time Decay", "U-Shaped", "W-Shaped"]',
        description="Available attribution models",
        category="analytics",
        organization_id=None,
        created_at=datetime.now()
    ),
    
    # Automation Configs
    MarketingConfig(
        id=15,
        key="workflow_statuses",
        value='["Draft", "Active", "Paused", "Completed", "Error"]',
        description="Available workflow statuses",
        category="automation",
        organization_id=None,
        created_at=datetime.now()
    ),
    MarketingConfig(
        id=16,
        key="trigger_types",
        value='["Form Submission", "Email Open", "Email Click", "Website Visit", "Download", "Purchase", "Webinar Attendance", "Custom Event"]',
        description="Available trigger types",
        category="automation",
        organization_id=None,
        created_at=datetime.now()
    ),
    
    # Segmentation Configs
    MarketingConfig(
        id=17,
        key="segment_types",
        value='["Dynamic", "Static", "Account-Based"]',
        description="Available segment types",
        category="segmentation",
        organization_id=None,
        created_at=datetime.now()
    ),
    MarketingConfig(
        id=18,
        key="segment_criteria_types",
        value='["Demographic", "Behavioral", "Firmographic", "Technographic", "Custom"]',
        description="Available segment criteria types",
        category="segmentation",
        organization_id=None,
        created_at=datetime.now()
    ),
    
    # Events Configs
    MarketingConfig(
        id=19,
        key="event_statuses",
        value='["Draft", "Planned", "Registration Open", "Upcoming", "Ongoing", "Completed", "Cancelled"]',
        description="Available event statuses",
        category="events",
        organization_id=None,
        created_at=datetime.now()
    ),
    MarketingConfig(
        id=20,
        key="event_types",
        value='["Webinar", "Conference", "Trade Show", "Workshop", "Networking Event", "Product Launch", "Virtual Event", "Other"]',
        description="Available event types",
        category="events",
        organization_id=None,
        created_at=datetime.now()
    ),
    
    # Partners Configs
    MarketingConfig(
        id=21,
        key="partner_statuses",
        value='["Active", "Inactive", "Pending", "Suspended"]',
        description="Available partner statuses",
        category="partners",
        organization_id=None,
        created_at=datetime.now()
    ),
    MarketingConfig(
        id=22,
        key="partner_types",
        value='["Reseller", "Distributor", "Affiliate", "Technology Partner", "Strategic Partner", "Other"]',
        description="Available partner types",
        category="partners",
        organization_id=None,
        created_at=datetime.now()
    ),
    
    # Resources Configs
    MarketingConfig(
        id=23,
        key="budget_statuses",
        value='["Draft", "Approved", "Active", "Completed", "Cancelled"]',
        description="Available budget statuses",
        category="resources",
        organization_id=None,
        created_at=datetime.now()
    ),
    MarketingConfig(
        id=24,
        key="budget_categories",
        value='["Campaigns", "Content", "Events", "Technology", "Personnel", "Agency Fees", "Other"]',
        description="Available budget categories",
        category="resources",
        organization_id=None,
        created_at=datetime.now()
    ),
    
    # CDP Configs
    MarketingConfig(
        id=25,
        key="data_source_types",
        value='["CRM", "Website", "Email", "Social Media", "Mobile App", "Offline", "Third Party", "Other"]',
        description="Available data source types",
        category="cdp",
        organization_id=None,
        created_at=datetime.now()
    ),
    MarketingConfig(
        id=26,
        key="identity_resolution_statuses",
        value='["Pending", "Matched", "Merged", "Conflicted"]',
        description="Available identity resolution statuses",
        category="cdp",
        organization_id=None,
        created_at=datetime.now()
    )
]

@router.get("/", response_model=List[MarketingConfig])
def list_marketing_configs(category: Optional[str] = None, organization_id: Optional[int] = None):
    """List all marketing configurations, optionally filtered by category or organization"""
    result = marketing_config_db
    
    if category:
        result = [config for config in result if config.category == category]
    
    if organization_id is not None:
        # Include both global configs (organization_id=None) and org-specific configs
        result = [config for config in result if config.organization_id is None or config.organization_id == organization_id]
    
    return result

@router.get("/{config_id}", response_model=MarketingConfig)
def get_marketing_config(config_id: int):
    """Get a specific marketing configuration by ID"""
    for config in marketing_config_db:
        if config.id == config_id:
            return config
    raise HTTPException(status_code=404, detail="Marketing configuration not found")

@router.post("/", response_model=MarketingConfig)
def create_marketing_config(config: MarketingConfigCreate):
    """Create a new marketing configuration"""
    new_id = max([c.id for c in marketing_config_db]) + 1 if marketing_config_db else 1
    new_config = MarketingConfig(
        id=new_id,
        created_at=datetime.now(),
        **config.dict()
    )
    marketing_config_db.append(new_config)
    return new_config

@router.put("/{config_id}", response_model=MarketingConfig)
def update_marketing_config(config_id: int, config_update: MarketingConfigUpdate):
    """Update an existing marketing configuration"""
    for index, config in enumerate(marketing_config_db):
        if config.id == config_id:
            updated_config = MarketingConfig(
                id=config_id,
                created_at=config.created_at,
                updated_at=datetime.now(),
                **config_update.dict()
            )
            marketing_config_db[index] = updated_config
            return updated_config
    raise HTTPException(status_code=404, detail="Marketing configuration not found")

@router.delete("/{config_id}")
def delete_marketing_config(config_id: int):
    """Delete a marketing configuration"""
    for index, config in enumerate(marketing_config_db):
        if config.id == config_id:
            del marketing_config_db[index]
            return {"message": "Marketing configuration deleted successfully"}
    raise HTTPException(status_code=404, detail="Marketing configuration not found")

@router.get("/key/{key}", response_model=MarketingConfig)
def get_marketing_config_by_key(key: str, organization_id: Optional[int] = None):
    """Get a marketing configuration by key, with optional organization override"""
    # First check for organization-specific config
    if organization_id is not None:
        for config in marketing_config_db:
            if config.key == key and config.organization_id == organization_id:
                return config
    
    # If no org-specific config found, return global config
    for config in marketing_config_db:
        if config.key == key and config.organization_id is None:
            return config
    
    raise HTTPException(status_code=404, detail=f"Marketing configuration with key '{key}' not found")

@router.get("/categories", response_model=List[str])
def list_categories():
    """List all marketing configuration categories"""
    categories = list(set([config.category for config in marketing_config_db]))
    return categories