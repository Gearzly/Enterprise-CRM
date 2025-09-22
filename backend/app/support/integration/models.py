from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class IntegrationType(str, Enum):
    crm = "CRM"
    ecommerce = "E-commerce"
    productivity = "Productivity"
    custom = "Custom"

class IntegrationStatus(str, Enum):
    active = "Active"
    inactive = "Inactive"
    error = "Error"
    pending = "Pending"

class IntegrationPlatform(str, Enum):
    salesforce = "Salesforce"
    hubspot = "HubSpot"
    shopify = "Shopify"
    woocommerce = "WooCommerce"
    slack = "Slack"
    microsoft_teams = "Microsoft Teams"
    custom = "Custom"

class IntegrationBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: IntegrationType
    platform: IntegrationPlatform
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    webhook_url: Optional[str] = None
    is_active: bool = True

class IntegrationCreate(IntegrationBase):
    pass

class IntegrationUpdate(IntegrationBase):
    pass

class Integration(IntegrationBase):
    id: int
    status: IntegrationStatus = IntegrationStatus.pending
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_sync_at: Optional[datetime] = None
    error_message: Optional[str] = None

class IntegrationMappingBase(BaseModel):
    integration_id: int
    source_field: str
    target_field: str
    data_type: str
    is_required: bool = False

class IntegrationMappingCreate(IntegrationMappingBase):
    pass

class IntegrationMappingUpdate(IntegrationMappingBase):
    pass

class IntegrationMapping(IntegrationMappingBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class SyncLogBase(BaseModel):
    integration_id: int
    sync_type: str
    record_count: int
    success_count: int
    failure_count: int
    duration_seconds: int

class SyncLogCreate(SyncLogBase):
    pass

class SyncLog(SyncLogBase):
    id: int
    created_at: datetime
    details: Optional[str] = None

class WebhookEventBase(BaseModel):
    integration_id: int
    event_type: str
    payload: Dict[str, Any]
    processed: bool = False

class WebhookEventCreate(WebhookEventBase):
    pass

class WebhookEvent(WebhookEventBase):
    id: int
    created_at: datetime
    processed_at: Optional[datetime] = None