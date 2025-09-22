from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class TicketPriority(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"
    urgent = "Urgent"

class TicketStatus(str, Enum):
    new = "New"
    in_progress = "In Progress"
    resolved = "Resolved"
    closed = "Closed"
    reopened = "Reopened"

class TicketChannel(str, Enum):
    email = "Email"
    web = "Web"
    phone = "Phone"
    chat = "Chat"

class TicketBase(BaseModel):
    subject: str
    description: Optional[str] = None
    priority: TicketPriority = TicketPriority.medium
    status: TicketStatus = TicketStatus.new
    channel: TicketChannel = TicketChannel.web
    assigned_to: Optional[str] = None
    customer_id: int
    tags: List[str] = []

class TicketCreate(TicketBase):
    pass

class TicketUpdate(TicketBase):
    pass

class Ticket(TicketBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None

class SLABase(BaseModel):
    name: str
    description: Optional[str] = None
    response_time_hours: int
    resolution_time_hours: int
    is_active: bool = True

class SLACreate(SLABase):
    pass

class SLAUpdate(SLABase):
    pass

class SLA(SLABase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None