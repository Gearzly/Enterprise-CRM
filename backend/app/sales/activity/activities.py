from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime
from .models import (
    Activity, ActivityCreate, ActivityUpdate, ActivityType, ActivityStatus
)
from .config import (
    get_activity_types, get_activity_statuses
)

router = APIRouter()

# In-memory storage for demo purposes
activities_db = [
    Activity(
        id=1,
        title="Intro Call",
        description="Initial introduction call with potential client",
        activity_type=ActivityType.call,
        status=ActivityStatus.completed,
        start_time=datetime.now(),
        end_time=datetime.now(),
        related_to="contact",
        related_id=1,
        assigned_to="John Sales",
        notes="Client interested in enterprise solution",
        created_at=datetime.now()
    ),
    Activity(
        id=2,
        title="Product Demo",
        description="Demonstration of our product features",
        activity_type=ActivityType.meeting,
        status=ActivityStatus.pending,
        start_time=datetime.now(),
        end_time=datetime.now(),
        related_to="lead",
        related_id=1,
        assigned_to="Jane Sales",
        notes="Scheduled for next week",
        created_at=datetime.now()
    )
]

@router.get("/", response_model=List[Activity])
def list_activities():
    return activities_db

@router.get("/{activity_id}", response_model=Activity)
def get_activity(activity_id: int):
    for activity in activities_db:
        if activity.id == activity_id:
            return activity
    raise HTTPException(status_code=404, detail="Activity not found")

@router.post("/", response_model=Activity)
def create_activity(activity: ActivityCreate):
    new_id = max([a.id for a in activities_db]) + 1 if activities_db else 1
    new_activity = Activity(
        id=new_id,
        created_at=datetime.now(),
        **activity.dict()
    )
    activities_db.append(new_activity)
    return new_activity

@router.put("/{activity_id}", response_model=Activity)
def update_activity(activity_id: int, activity_update: ActivityUpdate):
    for index, activity in enumerate(activities_db):
        if activity.id == activity_id:
            updated_activity = Activity(
                id=activity_id,
                created_at=activity.created_at,
                updated_at=datetime.now(),
                **activity_update.dict()
            )
            activities_db[index] = updated_activity
            return updated_activity
    raise HTTPException(status_code=404, detail="Activity not found")

@router.delete("/{activity_id}")
def delete_activity(activity_id: int):
    for index, activity in enumerate(activities_db):
        if activity.id == activity_id:
            del activities_db[index]
            return {"message": "Activity deleted successfully"}
    raise HTTPException(status_code=404, detail="Activity not found")

@router.get("/type/{activity_type}", response_model=List[Activity])
def get_activities_by_type(activity_type: str):
    """Get activities by type"""
    return [activity for activity in activities_db if activity.activity_type.value.lower() == activity_type.lower()]

@router.get("/status/{status}", response_model=List[Activity])
def get_activities_by_status(status: str):
    """Get activities by status"""
    return [activity for activity in activities_db if activity.status.value.lower() == status.lower()]

@router.get("/assigned/{assigned_to}", response_model=List[Activity])
def get_activities_by_assignee(assigned_to: str):
    """Get activities by assignee"""
    return [activity for activity in activities_db if activity.assigned_to and activity.assigned_to.lower() == assigned_to.lower()]

@router.get("/related/{related_to}/{related_id}", response_model=List[Activity])
def get_activities_by_related(related_to: str, related_id: int):
    """Get activities by related entity"""
    return [activity for activity in activities_db if activity.related_to == related_to and activity.related_id == related_id]

@router.get("/upcoming/{days}", response_model=List[Activity])
def get_upcoming_activities(days: int):
    """Get activities scheduled in the next N days"""
    from datetime import datetime, timedelta
    cutoff_date = datetime.now() + timedelta(days=days)
    return [activity for activity in activities_db if activity.start_time and activity.start_time <= cutoff_date and activity.start_time >= datetime.now()]

@router.get("/recent/{days}", response_model=List[Activity])
def get_recent_activities(days: int):
    """Get activities completed in the last N days"""
    from datetime import datetime, timedelta
    cutoff_date = datetime.now() - timedelta(days=days)
    return [activity for activity in activities_db if activity.created_at >= cutoff_date]

@router.get("/config/types", response_model=List[str])
def get_activity_type_options():
    """Get available activity types"""
    return get_activity_types()

@router.get("/config/statuses", response_model=List[str])
def get_activity_status_options():
    """Get available activity statuses"""
    return get_activity_statuses()