from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class EventBase(BaseModel):
    name: str
    description: Optional[str] = None
    event_type: str
    status: str = "Draft"
    start_date: datetime
    end_date: datetime
    location: Optional[str] = None
    is_virtual: bool = False
    virtual_link: Optional[str] = None
    capacity: Optional[int] = None
    registration_open_date: Optional[datetime] = None
    registration_close_date: Optional[datetime] = None
    tags: List[str] = []

class EventCreate(EventBase):
    pass

class EventUpdate(EventBase):
    pass

class Event(EventBase):
    id: int
    registered_count: int = 0
    attended_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

class RegistrationBase(BaseModel):
    event_id: int
    attendee_name: str
    attendee_email: str
    attendee_company: Optional[str] = None
    attendee_title: Optional[str] = None
    registration_date: datetime
    is_confirmed: bool = False
    confirmation_code: Optional[str] = None

class RegistrationCreate(RegistrationBase):
    pass

class RegistrationUpdate(RegistrationBase):
    pass

class Registration(RegistrationBase):
    id: int
    check_in_time: Optional[datetime] = None
    feedback: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

class EventPromotionBase(BaseModel):
    event_id: int
    name: str
    description: Optional[str] = None
    channels: List[str] = []  # e.g., ["email", "social_media", "website"]
    start_date: datetime
    end_date: datetime
    budget: Optional[float] = None
    is_active: bool = True

class EventPromotionCreate(EventPromotionBase):
    pass

class EventPromotionUpdate(EventPromotionBase):
    pass

class EventPromotion(EventPromotionBase):
    id: int
    reach: int = 0
    clicks: int = 0
    conversions: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

class AttendeeEngagementBase(BaseModel):
    event_id: int
    registration_id: int
    engagement_type: str  # e.g., "session_attended", "material_downloaded", "question_asked"
    engagement_time: datetime
    details: Optional[str] = None

class AttendeeEngagementCreate(AttendeeEngagementBase):
    pass

class AttendeeEngagementUpdate(AttendeeEngagementBase):
    pass

class AttendeeEngagement(AttendeeEngagementBase):
    id: int

class PostEventFollowUpBase(BaseModel):
    event_id: int
    name: str
    description: Optional[str] = None
    send_date: datetime
    recipients: List[str] = []  # Email addresses
    content: str  # Email content or template ID
    is_sent: bool = False

class PostEventFollowUpCreate(PostEventFollowUpBase):
    pass

class PostEventFollowUpUpdate(PostEventFollowUpBase):
    pass

class PostEventFollowUp(PostEventFollowUpBase):
    id: int
    sent_date: Optional[datetime] = None
    open_count: int = 0
    click_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None