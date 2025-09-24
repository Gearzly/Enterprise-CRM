from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from .models import (
    Integration, IntegrationCreate, IntegrationUpdate,
    IntegrationMapping, IntegrationMappingCreate, IntegrationMappingUpdate,
    SyncLog, SyncLogCreate,
    WebhookEvent, WebhookEventCreate
)
from .config import (
    get_integration_types, get_integration_platforms, get_integration_statuses,
    get_default_integration_type, get_default_integration_platform, get_sync_frequency_minutes
)

router = APIRouter(prefix="/integration", tags=["integration"])

# In-memory storage for demo purposes
integrations_db = []
integration_mappings_db = []
sync_logs_db = []
webhook_events_db = []

@router.get("/")
def get_integration_dashboard():
    """Get support integration dashboard with summary statistics"""
    return {
        "message": "Support Integration Dashboard",
        "statistics": {
            "total_integrations": len(integrations_db),
            "active_integrations": len([i for i in integrations_db if i.is_active]),
            "sync_logs": len(sync_logs_db),
            "webhook_events": len(webhook_events_db)
        }
    }

@router.get("/dashboard")
def get_integration_dashboard():
    """Get support integration dashboard with summary statistics"""
    return {
        "message": "Support Integration Dashboard",
        "statistics": {
            "total_integrations": len(integrations_db),
            "active_integrations": len([i for i in integrations_db if i.is_active]),
            "sync_logs": len(sync_logs_db),
            "webhook_events": len(webhook_events_db)
        }
    }

@router.get("/integrations", response_model=List[Integration])
def list_integrations():
    """List all integrations"""
    return integrations_db

@router.get("/{integration_id}", response_model=Integration)
def get_integration(integration_id: int):
    """Get a specific integration by ID"""
    for integration in integrations_db:
        if integration.id == integration_id:
            return integration
    raise HTTPException(status_code=404, detail="Integration not found")

@router.post("/", response_model=Integration)
def create_integration(integration: IntegrationCreate):
    """Create a new integration"""
    new_id = max([i.id for i in integrations_db]) + 1 if integrations_db else 1
    new_integration = Integration(
        id=new_id,
        created_at=datetime.now(),
        **integration.dict()
    )
    integrations_db.append(new_integration)
    return new_integration

@router.put("/{integration_id}", response_model=Integration)
def update_integration(integration_id: int, integration_update: IntegrationUpdate):
    """Update an existing integration"""
    for index, integration in enumerate(integrations_db):
        if integration.id == integration_id:
            updated_integration = Integration(
                id=integration_id,
                created_at=integration.created_at,
                updated_at=datetime.now(),
                **integration_update.dict()
            )
            integrations_db[index] = updated_integration
            return updated_integration
    raise HTTPException(status_code=404, detail="Integration not found")

@router.delete("/{integration_id}")
def delete_integration(integration_id: int):
    """Delete an integration"""
    for index, integration in enumerate(integrations_db):
        if integration.id == integration_id:
            del integrations_db[index]
            return {"message": "Integration deleted successfully"}
    raise HTTPException(status_code=404, detail="Integration not found")

@router.post("/{integration_id}/activate")
def activate_integration(integration_id: int):
    """Activate an integration"""
    for index, integration in enumerate(integrations_db):
        if integration.id == integration_id:
            integrations_db[index].is_active = True
            integrations_db[index].status = "Active"
            return {"message": "Integration activated successfully"}
    raise HTTPException(status_code=404, detail="Integration not found")

@router.post("/{integration_id}/deactivate")
def deactivate_integration(integration_id: int):
    """Deactivate an integration"""
    for index, integration in enumerate(integrations_db):
        if integration.id == integration_id:
            integrations_db[index].is_active = False
            integrations_db[index].status = "Inactive"
            return {"message": "Integration deactivated successfully"}
    raise HTTPException(status_code=404, detail="Integration not found")

@router.post("/{integration_id}/test")
def test_integration(integration_id: int):
    """Test an integration connection"""
    for index, integration in enumerate(integrations_db):
        if integration.id == integration_id:
            # In a real implementation, this would test the actual connection
            # For now, we'll just simulate a successful test
            integrations_db[index].status = "Active"
            return {"message": "Integration test successful"}
    raise HTTPException(status_code=404, detail="Integration not found")

@router.post("/{integration_id}/sync")
def sync_integration(integration_id: int):
    """Sync data with an integration"""
    for index, integration in enumerate(integrations_db):
        if integration.id == integration_id:
            start_time = datetime.now()
            # In a real implementation, this would sync actual data
            # For now, we'll just simulate a sync
            integrations_db[index].last_sync_at = datetime.now()
            integrations_db[index].status = "Active"
            
            # Create a sync log
            end_time = datetime.now()
            duration = (end_time - start_time).seconds
            sync_log = SyncLog(
                id=max([s.id for s in sync_logs_db]) + 1 if sync_logs_db else 1,
                integration_id=integration_id,
                sync_type="manual",
                record_count=100,
                success_count=95,
                failure_count=5,
                duration_seconds=duration,
                created_at=start_time,
                details="Manual sync completed with 5 failures"
            )
            sync_logs_db.append(sync_log)
            
            return {"message": "Integration sync completed successfully"}
    raise HTTPException(status_code=404, detail="Integration not found")

@router.get("/type/{type}", response_model=List[Integration])
def get_integrations_by_type(type: str):
    """Get integrations by type"""
    # Normalize the type parameter to handle case differences
    normalized_type = type.lower().title()
    return [integration for integration in integrations_db if integration.type == normalized_type]

@router.get("/platform/{platform}", response_model=List[Integration])
def get_integrations_by_platform(platform: str):
    """Get integrations by platform"""
    # Normalize the platform parameter to handle case differences
    normalized_platform = platform.lower().title()
    return [integration for integration in integrations_db if integration.platform == normalized_platform]

@router.get("/status/{status}", response_model=List[Integration])
def get_integrations_by_status(status: str):
    """Get integrations by status"""
    # Normalize the status parameter to handle case differences
    normalized_status = status.lower().title()
    return [integration for integration in integrations_db if integration.status == normalized_status]

# Integration Mapping endpoints
@router.get("/mappings", response_model=List[IntegrationMapping])
def list_integration_mappings():
    """List all integration mappings"""
    return integration_mappings_db

@router.get("/mappings/{mapping_id}", response_model=IntegrationMapping)
def get_integration_mapping(mapping_id: int):
    """Get a specific integration mapping by ID"""
    for mapping in integration_mappings_db:
        if mapping.id == mapping_id:
            return mapping
    raise HTTPException(status_code=404, detail="Integration mapping not found")

@router.post("/mappings", response_model=IntegrationMapping)
def create_integration_mapping(mapping: IntegrationMappingCreate):
    """Create a new integration mapping"""
    new_id = max([m.id for m in integration_mappings_db]) + 1 if integration_mappings_db else 1
    new_mapping = IntegrationMapping(
        id=new_id,
        created_at=datetime.now(),
        **mapping.dict()
    )
    integration_mappings_db.append(new_mapping)
    return new_mapping

@router.put("/mappings/{mapping_id}", response_model=IntegrationMapping)
def update_integration_mapping(mapping_id: int, mapping_update: IntegrationMappingUpdate):
    """Update an existing integration mapping"""
    for index, mapping in enumerate(integration_mappings_db):
        if mapping.id == mapping_id:
            updated_mapping = IntegrationMapping(
                id=mapping_id,
                created_at=mapping.created_at,
                updated_at=datetime.now(),
                **mapping_update.dict()
            )
            integration_mappings_db[index] = updated_mapping
            return updated_mapping
    raise HTTPException(status_code=404, detail="Integration mapping not found")

@router.delete("/mappings/{mapping_id}")
def delete_integration_mapping(mapping_id: int):
    """Delete an integration mapping"""
    for index, mapping in enumerate(integration_mappings_db):
        if mapping.id == mapping_id:
            del integration_mappings_db[index]
            return {"message": "Integration mapping deleted successfully"}
    raise HTTPException(status_code=404, detail="Integration mapping not found")

@router.get("/integrations/{integration_id}/mappings", response_model=List[IntegrationMapping])
def get_mappings_for_integration(integration_id: int):
    """Get mappings for a specific integration"""
    return [mapping for mapping in integration_mappings_db if mapping.integration_id == integration_id]

# Sync Log endpoints
@router.get("/logs", response_model=List[SyncLog])
def list_sync_logs():
    """List all sync logs"""
    return sync_logs_db

@router.get("/logs/{log_id}", response_model=SyncLog)
def get_sync_log(log_id: int):
    """Get a specific sync log by ID"""
    for log in sync_logs_db:
        if log.id == log_id:
            return log
    raise HTTPException(status_code=404, detail="Sync log not found")

@router.post("/logs", response_model=SyncLog)
def create_sync_log(log: SyncLogCreate):
    """Create a new sync log"""
    new_id = max([l.id for l in sync_logs_db]) + 1 if sync_logs_db else 1
    new_log = SyncLog(
        id=new_id,
        created_at=datetime.now(),
        **log.dict()
    )
    sync_logs_db.append(new_log)
    return new_log

@router.get("/integrations/{integration_id}/logs", response_model=List[SyncLog])
def get_logs_for_integration(integration_id: int):
    """Get sync logs for a specific integration"""
    return [log for log in sync_logs_db if log.integration_id == integration_id]

@router.get("/logs/recent", response_model=List[SyncLog])
def get_recent_sync_logs(limit: int = 10):
    """Get recent sync logs"""
    sorted_logs = sorted(sync_logs_db, key=lambda x: x.created_at, reverse=True)
    return sorted_logs[:limit]

# Webhook Event endpoints
@router.get("/webhooks", response_model=List[WebhookEvent])
def list_webhook_events():
    """List all webhook events"""
    return webhook_events_db

@router.get("/webhooks/{event_id}", response_model=WebhookEvent)
def get_webhook_event(event_id: int):
    """Get a specific webhook event by ID"""
    for event in webhook_events_db:
        if event.id == event_id:
            return event
    raise HTTPException(status_code=404, detail="Webhook event not found")

@router.post("/webhooks", response_model=WebhookEvent)
def create_webhook_event(event: WebhookEventCreate):
    """Create a new webhook event"""
    new_id = max([w.id for w in webhook_events_db]) + 1 if webhook_events_db else 1
    new_event = WebhookEvent(
        id=new_id,
        created_at=datetime.now(),
        **event.dict()
    )
    webhook_events_db.append(new_event)
    return new_event

@router.put("/webhooks/{event_id}/process")
def process_webhook_event(event_id: int):
    """Mark a webhook event as processed"""
    for index, event in enumerate(webhook_events_db):
        if event.id == event_id:
            webhook_events_db[index].processed = True
            webhook_events_db[index].processed_at = datetime.now()
            return {"message": "Webhook event processed successfully"}
    raise HTTPException(status_code=404, detail="Webhook event not found")

@router.get("/webhooks/unprocessed", response_model=List[WebhookEvent])
def get_unprocessed_webhook_events():
    """Get all unprocessed webhook events"""
    return [event for event in webhook_events_db if not event.processed]

@router.get("/integrations/{integration_id}/webhooks", response_model=List[WebhookEvent])
def get_webhooks_for_integration(integration_id: int):
    """Get webhook events for a specific integration"""
    return [event for event in webhook_events_db if event.integration_id == integration_id]

# Configuration endpoints
@router.get("/config/types", response_model=List[str])
def get_integration_type_options():
    """Get available integration type options"""
    return get_integration_types()

@router.get("/config/platforms", response_model=List[str])
def get_integration_platform_options():
    """Get available integration platform options"""
    return get_integration_platforms()

@router.get("/config/statuses", response_model=List[str])
def get_integration_status_options():
    """Get available integration status options"""
    return get_integration_statuses()

@router.get("/config/sync-frequency", response_model=int)
def get_sync_frequency():
    """Get sync frequency in minutes"""
    return get_sync_frequency_minutes()