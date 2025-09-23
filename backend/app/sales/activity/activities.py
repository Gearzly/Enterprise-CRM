from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .models import (
    Activity, ActivityCreate, ActivityUpdate, ActivityType, ActivityStatus
)
from .config import (
    get_activity_types, get_activity_statuses
)
from app.core.deps import get_db
from app.core.crud import activity as crud_activity

router = APIRouter()

@router.get("/", response_model=List[Activity])
def list_activities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all activities"""
    activities = crud_activity.get_multi(db, skip=skip, limit=limit)
    return activities

@router.get("/{activity_id}", response_model=Activity)
def get_activity(activity_id: int, db: Session = Depends(get_db)):
    """Get a specific activity by ID"""
    db_activity = crud_activity.get(db, id=activity_id)
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return db_activity

@router.post("/", response_model=Activity)
def create_activity(activity: ActivityCreate, db: Session = Depends(get_db)):
    """Create a new activity"""
    return crud_activity.create(db, obj_in=activity)

@router.put("/{activity_id}", response_model=Activity)
def update_activity(activity_id: int, activity_update: ActivityUpdate, db: Session = Depends(get_db)):
    """Update an existing activity"""
    db_activity = crud_activity.get(db, id=activity_id)
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return crud_activity.update(db, db_obj=db_activity, obj_in=activity_update)

@router.delete("/{activity_id}")
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    """Delete an activity"""
    db_activity = crud_activity.get(db, id=activity_id)
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    crud_activity.remove(db, id=activity_id)
    return {"message": "Activity deleted successfully"}

@router.get("/type/{activity_type}", response_model=List[Activity])
def get_activities_by_type(activity_type: str, db: Session = Depends(get_db)):
    """Get activities by type"""
    return crud_activity.get_by_type(db, activity_type=activity_type)

@router.get("/status/{status}", response_model=List[Activity])
def get_activities_by_status(status: str, db: Session = Depends(get_db)):
    """Get activities by status"""
    return crud_activity.get_by_status(db, status=status)

@router.get("/assigned/{assigned_to}", response_model=List[Activity])
def get_activities_by_assignee(assigned_to: str, db: Session = Depends(get_db)):
    """Get activities by assignee"""
    return crud_activity.get_by_assigned_to(db, assigned_to=assigned_to)

@router.get("/related/{related_to}/{related_id}", response_model=List[Activity])
def get_activities_by_related(related_to: str, related_id: int, db: Session = Depends(get_db)):
    """Get activities by related entity"""
    return crud_activity.get_by_related(db, related_to=related_to, related_id=related_id)

@router.get("/upcoming/{days}", response_model=List[Activity])
def get_upcoming_activities(days: int, db: Session = Depends(get_db)):
    """Get activities scheduled in the next N days"""
    return crud_activity.get_upcoming(db, days=days)

@router.get("/recent/{days}", response_model=List[Activity])
def get_recent_activities(days: int, db: Session = Depends(get_db)):
    """Get activities completed in the last N days"""
    return crud_activity.get_recent(db, days=days)

@router.get("/config/types", response_model=List[str])
def get_activity_type_options():
    """Get available activity types"""
    return get_activity_types()

@router.get("/config/statuses", response_model=List[str])
def get_activity_status_options():
    """Get available activity statuses"""
    return get_activity_statuses()