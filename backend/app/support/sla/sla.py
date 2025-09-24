from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from .models import (
    SLA, SLACreate, SLAUpdate,
    SLABreach, SLABreachCreate, SLABreachUpdate,
    SLANotification, SLANotificationCreate, SLANotificationUpdate
)
from .config import (
    get_sla_types, get_default_sla_type, 
    get_default_response_time_hours, get_max_notification_threshold
)
from app.core.deps import get_db
from app.core.crud import sla as crud_sla

router = APIRouter(prefix="/sla", tags=["sla"])

@router.get("/")
def get_sla_dashboard(db: Session = Depends(get_db)):
    """Get support SLA dashboard with summary statistics"""
    all_slas = crud_sla.sla.get_multi(db)
    all_breaches = crud_sla.sla_breach.get_multi(db)
    all_notifications = crud_sla.sla_notification.get_multi(db)
    active_slas = crud_sla.sla.get_active_slas(db)
    
    return {
        "message": "Support SLA Dashboard",
        "statistics": {
            "total_slas": len(all_slas),
            "total_breaches": len(all_breaches),
            "total_notifications": len(all_notifications),
            "active_slas": len(active_slas)
        }
    }

@router.get("/sla", response_model=List[SLA])
def list_slas(db: Session = Depends(get_db)):
    """List all SLAs"""
    return crud_sla.sla.get_multi(db)

@router.get("/{sla_id}", response_model=SLA)
def get_sla(sla_id: int, db: Session = Depends(get_db)):
    """Get a specific SLA by ID"""
    sla = crud_sla.sla.get(db=db, id=sla_id)
    if not sla:
        raise HTTPException(status_code=404, detail="SLA not found")
    return sla

@router.post("/", response_model=SLA)
def create_sla(sla: SLACreate, db: Session = Depends(get_db)):
    """Create a new SLA"""
    return crud_sla.sla.create(db=db, obj_in=sla)

@router.put("/{sla_id}", response_model=SLA)
def update_sla(sla_id: int, sla_update: SLAUpdate, db: Session = Depends(get_db)):
    """Update an existing SLA"""
    sla = crud_sla.sla.get(db=db, id=sla_id)
    if not sla:
        raise HTTPException(status_code=404, detail="SLA not found")
    return crud_sla.sla.update(db=db, db_obj=sla, obj_in=sla_update)

@router.delete("/{sla_id}")
def delete_sla(sla_id: int, db: Session = Depends(get_db)):
    """Delete an SLA"""
    sla = crud_sla.sla.get(db=db, id=sla_id)
    if not sla:
        raise HTTPException(status_code=404, detail="SLA not found")
    crud_sla.sla.remove(db=db, id=sla_id)
    return {"message": "SLA deleted successfully"}

@router.post("/{sla_id}/activate")
def activate_sla(sla_id: int, db: Session = Depends(get_db)):
    """Activate an SLA"""
    return crud_sla.sla.activate_sla(db=db, sla_id=sla_id)

@router.post("/{sla_id}/deactivate")
def deactivate_sla(sla_id: int, db: Session = Depends(get_db)):
    """Deactivate an SLA"""
    return crud_sla.sla.deactivate_sla(db=db, sla_id=sla_id)

@router.get("/slas/type/{type}", response_model=List[SLA])
def get_slas_by_type(type: str, db: Session = Depends(get_db)):
    """Get SLAs by type"""
    return crud_sla.sla.get_by_type(db=db, sla_type=type)

@router.get("/active", response_model=List[SLA])
def get_active_slas(db: Session = Depends(get_db)):
    """Get all active SLAs"""
    return crud_sla.sla.get_active_slas(db)

# SLA Breach endpoints
@router.get("/breaches", response_model=List[SLABreach])
def list_sla_breaches(db: Session = Depends(get_db)):
    """List all SLA breaches"""
    return crud_sla.sla_breach.get_multi(db)

@router.get("/breaches/{breach_id}", response_model=SLABreach)
def get_sla_breach(breach_id: int, db: Session = Depends(get_db)):
    """Get a specific SLA breach by ID"""
    breach = crud_sla.sla_breach.get(db=db, id=breach_id)
    if not breach:
        raise HTTPException(status_code=404, detail="SLA breach not found")
    return breach

@router.post("/breaches", response_model=SLABreach)
def create_sla_breach(breach: SLABreachCreate, db: Session = Depends(get_db)):
    """Create a new SLA breach"""
    return crud_sla.sla_breach.create(db=db, obj_in=breach)

@router.put("/breaches/{breach_id}", response_model=SLABreach)
def update_sla_breach(breach_id: int, breach_update: SLABreachUpdate, db: Session = Depends(get_db)):
    """Update an existing SLA breach"""
    breach = crud_sla.sla_breach.get(db=db, id=breach_id)
    if not breach:
        raise HTTPException(status_code=404, detail="SLA breach not found")
    return crud_sla.sla_breach.update(db=db, db_obj=breach, obj_in=breach_update)

@router.delete("/breaches/{breach_id}")
def delete_sla_breach(breach_id: int, db: Session = Depends(get_db)):
    """Delete an SLA breach"""
    breach = crud_sla.sla_breach.get(db=db, id=breach_id)
    if not breach:
        raise HTTPException(status_code=404, detail="SLA breach not found")
    crud_sla.sla_breach.remove(db=db, id=breach_id)
    return {"message": "SLA breach deleted successfully"}

@router.post("/breaches/{breach_id}/resolve")
def resolve_sla_breach(breach_id: int, db: Session = Depends(get_db)):
    """Resolve an SLA breach"""
    return crud_sla.sla_breach.resolve_breach(db=db, breach_id=breach_id)

@router.get("/breaches/unresolved", response_model=List[SLABreach])
def get_unresolved_sla_breaches(db: Session = Depends(get_db)):
    """Get all unresolved SLA breaches"""
    return crud_sla.sla_breach.get_unresolved_breaches(db)

@router.get("/tickets/{ticket_id}/breaches", response_model=List[SLABreach])
def get_breaches_for_ticket(ticket_id: int, db: Session = Depends(get_db)):
    """Get SLA breaches for a specific ticket"""
    return crud_sla.sla_breach.get_breaches_for_ticket(db=db, ticket_id=ticket_id)

# SLA Notification endpoints
@router.get("/notifications", response_model=List[SLANotification])
def list_sla_notifications(db: Session = Depends(get_db)):
    """List all SLA notifications"""
    return crud_sla.sla_notification.get_multi(db)

@router.get("/notifications/{notification_id}", response_model=SLANotification)
def get_sla_notification(notification_id: int, db: Session = Depends(get_db)):
    """Get a specific SLA notification by ID"""
    notification = crud_sla.sla_notification.get(db=db, id=notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="SLA notification not found")
    return notification

@router.post("/notifications", response_model=SLANotification)
def create_sla_notification(notification: SLANotificationCreate, db: Session = Depends(get_db)):
    """Create a new SLA notification"""
    return crud_sla.sla_notification.create(db=db, obj_in=notification)

@router.put("/notifications/{notification_id}", response_model=SLANotification)
def update_sla_notification(notification_id: int, notification_update: SLANotificationUpdate, db: Session = Depends(get_db)):
    """Update an existing SLA notification"""
    notification = crud_sla.sla_notification.get(db=db, id=notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="SLA notification not found")
    return crud_sla.sla_notification.update(db=db, db_obj=notification, obj_in=notification_update)

@router.delete("/notifications/{notification_id}")
def delete_sla_notification(notification_id: int, db: Session = Depends(get_db)):
    """Delete an SLA notification"""
    notification = crud_sla.sla_notification.get(db=db, id=notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="SLA notification not found")
    crud_sla.sla_notification.remove(db=db, id=notification_id)
    return {"message": "SLA notification deleted successfully"}

@router.get("/sla/{sla_id}/notifications", response_model=List[SLANotification])
def get_notifications_for_sla(sla_id: int, db: Session = Depends(get_db)):
    """Get notifications for a specific SLA"""
    return crud_sla.sla_notification.get_notifications_for_sla(db=db, sla_id=sla_id)

# Configuration endpoints
@router.get("/config/types", response_model=List[str])
def get_sla_type_options():
    """Get available SLA type options"""
    return get_sla_types()

@router.get("/config/max-threshold", response_model=int)
def get_max_notification_threshold_value():
    """Get maximum notification threshold percentage"""
    return get_max_notification_threshold()