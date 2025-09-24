from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime
from .models import SupportConfig, SupportConfigCreate, SupportConfigUpdate

router = APIRouter()

# In-memory storage for demo purposes
support_config_db = [
    # Ticket Management Configs
    SupportConfig(
        id=1,
        key="ticket_priorities",
        value='["Low", "Medium", "High", "Urgent"]',
        description="Available ticket priorities",
        category="tickets",
        organization_id=None,
        created_at=datetime.now()
    ),
    SupportConfig(
        id=2,
        key="ticket_statuses",
        value='["New", "Open", "Pending", "Resolved", "Closed", "Escalated"]',
        description="Available ticket statuses",
        category="tickets",
        organization_id=None,
        created_at=datetime.now()
    ),
    SupportConfig(
        id=3,
        key="ticket_channels",
        value='["Email", "Phone", "Chat", "Portal", "Social Media"]',
        description="Available ticket channels",
        category="tickets",
        organization_id=None,
        created_at=datetime.now()
    ),
    
    # SLA Management Configs
    SupportConfig(
        id=4,
        key="sla_priorities",
        value='["Low", "Medium", "High", "Urgent"]',
        description="Available SLA priorities",
        category="sla",
        organization_id=None,
        created_at=datetime.now()
    ),
    
    # Knowledge Base Configs
    SupportConfig(
        id=5,
        key="kb_categories",
        value='["General", "Technical", "Billing", "Account", "Product", "Troubleshooting"]',
        description="Available knowledge base categories",
        category="knowledge_base",
        organization_id=None,
        created_at=datetime.now()
    ),
    
    # Interaction Configs
    SupportConfig(
        id=6,
        key="interaction_types",
        value='["Call", "Email", "Chat", "Meeting", "Note"]',
        description="Available interaction types",
        category="interactions",
        organization_id=None,
        created_at=datetime.now()
    ),
    
    # Live Chat Configs
    SupportConfig(
        id=7,
        key="chat_statuses",
        value='["Available", "Busy", "Away", "Offline"]',
        description="Available chat agent statuses",
        category="live_chat",
        organization_id=None,
        created_at=datetime.now()
    ),
    
    # Reporting Configs
    SupportConfig(
        id=8,
        key="report_types",
        value='["Ticket Volume", "Resolution Time", "Agent Performance", "Customer Satisfaction", "SLA Compliance", "Channel Performance"]',
        description="Available report types",
        category="reporting",
        organization_id=None,
        created_at=datetime.now()
    ),
]

@router.get("/", response_model=List[SupportConfig])
def list_support_configs(category: Optional[str] = None, organization_id: Optional[int] = None):
    """List all support configurations, optionally filtered by category or organization"""
    result = support_config_db
    
    if category:
        result = [config for config in result if config.category == category]
    
    if organization_id is not None:
        # Include both global configs (organization_id=None) and org-specific configs
        result = [config for config in result if config.organization_id is None or config.organization_id == organization_id]
    
    return result

@router.get("/{config_id}", response_model=SupportConfig)
def get_support_config(config_id: int):
    """Get a specific support configuration by ID"""
    for config in support_config_db:
        if config.id == config_id:
            return config
    raise HTTPException(status_code=404, detail="Support configuration not found")

@router.post("/", response_model=SupportConfig)
def create_support_config(config: SupportConfigCreate):
    """Create a new support configuration"""
    new_id = max([c.id for c in support_config_db]) + 1 if support_config_db else 1
    new_config = SupportConfig(
        id=new_id,
        created_at=datetime.now(),
        **config.dict()
    )
    support_config_db.append(new_config)
    return new_config

@router.put("/{config_id}", response_model=SupportConfig)
def update_support_config(config_id: int, config_update: SupportConfigUpdate):
    """Update an existing support configuration"""
    for index, config in enumerate(support_config_db):
        if config.id == config_id:
            updated_config = SupportConfig(
                id=config_id,
                created_at=config.created_at,
                updated_at=datetime.now(),
                **config_update.dict()
            )
            support_config_db[index] = updated_config
            return updated_config
    raise HTTPException(status_code=404, detail="Support configuration not found")

@router.delete("/{config_id}")
def delete_support_config(config_id: int):
    """Delete a support configuration"""
    for index, config in enumerate(support_config_db):
        if config.id == config_id:
            del support_config_db[index]
            return {"message": "Support configuration deleted successfully"}
    raise HTTPException(status_code=404, detail="Support configuration not found")

@router.get("/key/{key}", response_model=SupportConfig)
def get_support_config_by_key(key: str, organization_id: Optional[int] = None):
    """Get a support configuration by key, with optional organization override"""
    # First check for organization-specific config
    if organization_id is not None:
        for config in support_config_db:
            if config.key == key and config.organization_id == organization_id:
                return config
    
    # If no org-specific config found, return global config
    for config in support_config_db:
        if config.key == key and config.organization_id is None:
            return config
    
    raise HTTPException(status_code=404, detail=f"Support configuration with key '{key}' not found")

@router.get("/categories", response_model=List[str])
def list_categories():
    """List all support configuration categories"""
    categories = list(set([config.category for config in support_config_db]))
    return categories