from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class ActivityType(str, Enum):
    call = "Call"
    meeting = "Meeting"
    email = "Email"
    task = "Task"
    note = "Note"
    deadline = "Deadline"

class ActivityStatus(str, Enum):
    pending = "Pending"
    completed = "Completed"
    cancelled = "Cancelled"

class ActivityBase(BaseModel):
    title: str
    description: Optional[str] = None
    activity_type: ActivityType
    status: ActivityStatus = ActivityStatus.pending
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    related_to: Optional[str] = None  # Could be lead, contact, opportunity, etc.
    related_id: Optional[int] = None
    assigned_to: Optional[str] = None
    notes: Optional[str] = None

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(ActivityBase):
    pass

class Activity(ActivityBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None