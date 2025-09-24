from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime

class TicketBase(BaseModel):
    subject: str
    description: Optional[str] = None
    priority: str = "Medium"
    status: str = "New"
    channel: str = "Web"
    assigned_to: Optional[str] = None
    customer_id: int
    tags: List[str] = []

    @validator('priority')
    def validate_priority(cls, v):
        # In a real implementation, this would fetch from config
        # For now, we'll allow any string but validate against known values in the service layer
        return v

    @validator('status')
    def validate_status(cls, v):
        # In a real implementation, this would fetch from config
        # For now, we'll allow any string but validate against known values in the service layer
        return v

    @validator('channel')
    def validate_channel(cls, v):
        # In a real implementation, this would fetch from config
        # For now, we'll allow any string but validate against known values in the service layer
        return v

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