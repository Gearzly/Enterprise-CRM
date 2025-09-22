from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .models import (
    SLA, SLACreate, SLAUpdate,
    SLABreach, SLABreachCreate, SLABreachUpdate,
    SLANotification, SLANotificationCreate, SLANotificationUpdate
)
from .config import (
    get_sla_types, get_default_sla_type, 
    get_default_response_time_hours, get_max_notification_threshold
)

router = APIRouter()

# In-memory storage for demo purposes
slas_db = []
sla_breaches_db = []
sla_notifications_db = []

@router.get("/", response_model=List[SLA])
def list_slas():
    """List all SLAs"""
    return slas_db

@router.get("/{sla_id}", response_model=SLA)
def get_sla(sla_id: int):
    """Get a specific SLA by ID"""
    for sla in slas_db:
        if sla.id == sla_id:
            return sla
    raise HTTPException(status_code=404, detail="SLA not found")

@router.post("/", response_model=SLA)
def create_sla(sla: SLACreate):
    """Create a new SLA"""
    new_id = max([s.id for s in slas_db]) + 1 if slas_db else 1
    new_sla = SLA(
        id=new_id,
        created_at=datetime.now(),
        **sla.dict()
    )
    slas_db.append(new_sla)
    return new_sla

@router.put("/{sla_id}", response_model=SLA)
def update_sla(sla_id: int, sla_update: SLAUpdate):
    """Update an existing SLA"""
    for index, sla in enumerate(slas_db):
        if sla.id == sla_id:
            updated_sla = SLA(
                id=sla_id,
                created_at=sla.created_at,
                updated_at=datetime.now(),
                **sla_update.dict()
            )
            slas_db[index] = updated_sla
            return updated_sla
    raise HTTPException(status_code=404, detail="SLA not found")

@router.delete("/{sla_id}")
def delete_sla(sla_id: int):
    """Delete an SLA"""
    for index, sla in enumerate(slas_db):
        if sla.id == sla_id:
            del slas_db[index]
            return {"message": "SLA deleted successfully"}
    raise HTTPException(status_code=404, detail="SLA not found")

@router.post("/{sla_id}/activate")
def activate_sla(sla_id: int):
    """Activate an SLA"""
    for index, sla in enumerate(slas_db):
        if sla.id == sla_id:
            slas_db[index].is_active = True
            return {"message": "SLA activated successfully"}
    raise HTTPException(status_code=404, detail="SLA not found")

@router.post("/{sla_id}/deactivate")
def deactivate_sla(sla_id: int):
    """Deactivate an SLA"""
    for index, sla in enumerate(slas_db):
        if sla.id == sla_id:
            slas_db[index].is_active = False
            return {"message": "SLA deactivated successfully"}
    raise HTTPException(status_code=404, detail="SLA not found")

@router.get("/type/{type}", response_model=List[SLA])
def get_slas_by_type(type: str):
    """Get SLAs by type"""
    # Normalize the type parameter to handle case differences
    normalized_type = type.lower().title()
    return [sla for sla in slas_db if sla.type.value == normalized_type]

@router.get("/active", response_model=List[SLA])
def get_active_slas():
    """Get all active SLAs"""
    return [sla for sla in slas_db if sla.is_active]

# SLA Breach endpoints
@router.get("/breaches", response_model=List[SLABreach])
def list_sla_breaches():
    """List all SLA breaches"""
    return sla_breaches_db

@router.get("/breaches/{breach_id}", response_model=SLABreach)
def get_sla_breach(breach_id: int):
    """Get a specific SLA breach by ID"""
    for breach in sla_breaches_db:
        if breach.id == breach_id:
            return breach
    raise HTTPException(status_code=404, detail="SLA breach not found")

@router.post("/breaches", response_model=SLABreach)
def create_sla_breach(breach: SLABreachCreate):
    """Create a new SLA breach"""
    new_id = max([b.id for b in sla_breaches_db]) + 1 if sla_breaches_db else 1
    new_breach = SLABreach(
        id=new_id,
        created_at=datetime.now(),
        **breach.dict()
    )
    sla_breaches_db.append(new_breach)
    return new_breach

@router.put("/breaches/{breach_id}", response_model=SLABreach)
def update_sla_breach(breach_id: int, breach_update: SLABreachUpdate):
    """Update an existing SLA breach"""
    for index, breach in enumerate(sla_breaches_db):
        if breach.id == breach_id:
            updated_breach = SLABreach(
                id=breach_id,
                created_at=breach.created_at,
                updated_at=datetime.now(),
                **breach_update.dict()
            )
            sla_breaches_db[index] = updated_breach
            return updated_breach
    raise HTTPException(status_code=404, detail="SLA breach not found")

@router.delete("/breaches/{breach_id}")
def delete_sla_breach(breach_id: int):
    """Delete an SLA breach"""
    for index, breach in enumerate(sla_breaches_db):
        if breach.id == breach_id:
            del sla_breaches_db[index]
            return {"message": "SLA breach deleted successfully"}
    raise HTTPException(status_code=404, detail="SLA breach not found")

@router.post("/breaches/{breach_id}/resolve")
def resolve_sla_breach(breach_id: int):
    """Resolve an SLA breach"""
    for index, breach in enumerate(sla_breaches_db):
        if breach.id == breach_id:
            sla_breaches_db[index].resolved = True
            sla_breaches_db[index].resolved_at = datetime.now()
            return {"message": "SLA breach resolved successfully"}
    raise HTTPException(status_code=404, detail="SLA breach not found")

@router.get("/breaches/unresolved", response_model=List[SLABreach])
def get_unresolved_sla_breaches():
    """Get all unresolved SLA breaches"""
    return [breach for breach in sla_breaches_db if not breach.resolved]

@router.get("/tickets/{ticket_id}/breaches", response_model=List[SLABreach])
def get_breaches_for_ticket(ticket_id: int):
    """Get SLA breaches for a specific ticket"""
    return [breach for breach in sla_breaches_db if breach.ticket_id == ticket_id]

# SLA Notification endpoints
@router.get("/notifications", response_model=List[SLANotification])
def list_sla_notifications():
    """List all SLA notifications"""
    return sla_notifications_db

@router.get("/notifications/{notification_id}", response_model=SLANotification)
def get_sla_notification(notification_id: int):
    """Get a specific SLA notification by ID"""
    for notification in sla_notifications_db:
        if notification.id == notification_id:
            return notification
    raise HTTPException(status_code=404, detail="SLA notification not found")

@router.post("/notifications", response_model=SLANotification)
def create_sla_notification(notification: SLANotificationCreate):
    """Create a new SLA notification"""
    new_id = max([n.id for n in sla_notifications_db]) + 1 if sla_notifications_db else 1
    new_notification = SLANotification(
        id=new_id,
        created_at=datetime.now(),
        **notification.dict()
    )
    sla_notifications_db.append(new_notification)
    return new_notification

@router.put("/notifications/{notification_id}", response_model=SLANotification)
def update_sla_notification(notification_id: int, notification_update: SLANotificationUpdate):
    """Update an existing SLA notification"""
    for index, notification in enumerate(sla_notifications_db):
        if notification.id == notification_id:
            updated_notification = SLANotification(
                id=notification_id,
                created_at=notification.created_at,
                updated_at=datetime.now(),
                **notification_update.dict()
            )
            sla_notifications_db[index] = updated_notification
            return updated_notification
    raise HTTPException(status_code=404, detail="SLA notification not found")

@router.delete("/notifications/{notification_id}")
def delete_sla_notification(notification_id: int):
    """Delete an SLA notification"""
    for index, notification in enumerate(sla_notifications_db):
        if notification.id == notification_id:
            del sla_notifications_db[index]
            return {"message": "SLA notification deleted successfully"}
    raise HTTPException(status_code=404, detail="SLA notification not found")

@router.get("/sla/{sla_id}/notifications", response_model=List[SLANotification])
def get_notifications_for_sla(sla_id: int):
    """Get notifications for a specific SLA"""
    return [notification for notification in sla_notifications_db if notification.sla_id == sla_id]

# Configuration endpoints
@router.get("/config/types", response_model=List[str])
def get_sla_type_options():
    """Get available SLA type options"""
    return get_sla_types()

@router.get("/config/max-threshold", response_model=int)
def get_max_notification_threshold_value():
    """Get maximum notification threshold percentage"""
    return get_max_notification_threshold()