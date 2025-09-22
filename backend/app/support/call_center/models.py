from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class CallDirection(str, Enum):
    inbound = "Inbound"
    outbound = "Outbound"

class CallStatus(str, Enum):
    pending = "Pending"
    ringing = "Ringing"
    in_progress = "In Progress"
    completed = "Completed"
    missed = "Missed"
    voicemail = "Voicemail"

class CallPriority(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"

class CallBase(BaseModel):
    customer_id: int
    direction: CallDirection
    from_number: str
    to_number: str
    priority: CallPriority = CallPriority.medium
    assigned_agent_id: Optional[str] = None
    tags: List[str] = []

class CallCreate(CallBase):
    pass

class CallUpdate(CallBase):
    pass

class Call(CallBase):
    id: int
    status: CallStatus = CallStatus.pending
    created_at: datetime
    updated_at: Optional[datetime] = None
    answered_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None

class CallQueueBase(BaseModel):
    name: str
    description: Optional[str] = None
    max_wait_time_minutes: int = 5
    is_active: bool = True

class CallQueueCreate(CallQueueBase):
    pass

class CallQueueUpdate(CallQueueBase):
    pass

class CallQueue(CallQueueBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class IVRMenuBase(BaseModel):
    name: str
    description: Optional[str] = None
    digits: str  # The digits pressed to select this option
    action: str  # The action to take (e.g., "transfer", "menu", "voicemail")
    target: Optional[str] = None  # The target of the action (e.g., extension, queue name)
    is_active: bool = True

class IVRMenuCreate(IVRMenuBase):
    pass

class IVRMenuUpdate(IVRMenuBase):
    pass

class IVRMenu(IVRMenuBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None