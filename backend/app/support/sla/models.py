from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class SLAType(str, Enum):
    response = "Response"
    resolution = "Resolution"
    first_response = "First Response"

class SLAStatus(str, Enum):
    active = "Active"
    inactive = "Inactive"
    archived = "Archived"

class SLABase(BaseModel):
    name: str
    description: Optional[str] = None
    type: SLAType
    response_time_hours: int
    resolution_time_hours: Optional[int] = None
    is_active: bool = True
    priority: int = 1  # 1-5 scale

class SLACreate(SLABase):
    pass

class SLAUpdate(SLABase):
    pass

class SLA(SLABase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class SLABreachBase(BaseModel):
    sla_id: int
    ticket_id: int
    breach_reason: Optional[str] = None
    resolved: bool = False

class SLABreachCreate(SLABreachBase):
    pass

class SLABreachUpdate(SLABreachBase):
    pass

class SLABreach(SLABreachBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None

class SLANotificationBase(BaseModel):
    sla_id: int
    threshold_percentage: int  # Percentage of SLA time elapsed before notification
    notification_type: str  # email, sms, in_app
    recipient_type: str  # customer, agent, team
    message_template: str

class SLANotificationCreate(SLANotificationBase):
    pass

class SLANotificationUpdate(SLANotificationBase):
    pass

class SLANotification(SLANotificationBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None