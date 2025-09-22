from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter()

class ActivityBase(BaseModel):
    type: str
    subject: str
    description: Optional[str] = None
    date: Optional[datetime] = None
    duration: Optional[int] = None  # in minutes
    contact_id: Optional[int] = None
    lead_id: Optional[int] = None
    opportunity_id: Optional[int] = None

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(ActivityBase):
    pass

class Activity(ActivityBase):
    id: int

# In-memory storage for demo purposes
activities_db = [
    Activity(
        id=1,
        type="Call",
        subject="Intro Call",
        description="Initial introduction call with potential client",
        date=datetime.now(),
        duration=30,
        contact_id=1
    ),
    Activity(
        id=2,
        type="Meeting",
        subject="Product Demo",
        description="Demonstration of our product features",
        date=datetime.now(),
        duration=60,
        lead_id=1
    )
]

@router.get("/activities", response_model=List[Activity])
def list_activities():
    return activities_db

@router.get("/activities/{activity_id}", response_model=Activity)
def get_activity(activity_id: int):
    for activity in activities_db:
        if activity.id == activity_id:
            return activity
    raise HTTPException(status_code=404, detail="Activity not found")

@router.post("/activities", response_model=Activity)
def create_activity(activity: ActivityCreate):
    new_id = max([a.id for a in activities_db]) + 1 if activities_db else 1
    new_activity = Activity(id=new_id, **activity.dict())
    activities_db.append(new_activity)
    return new_activity

@router.put("/activities/{activity_id}", response_model=Activity)
def update_activity(activity_id: int, activity_update: ActivityUpdate):
    for index, activity in enumerate(activities_db):
        if activity.id == activity_id:
            updated_activity = Activity(id=activity_id, **activity_update.dict())
            activities_db[index] = updated_activity
            return updated_activity
    raise HTTPException(status_code=404, detail="Activity not found")

@router.delete("/activities/{activity_id}")
def delete_activity(activity_id: int):
    for index, activity in enumerate(activities_db):
        if activity.id == activity_id:
            del activities_db[index]
            return {"message": "Activity deleted successfully"}
    raise HTTPException(status_code=404, detail="Activity not found")