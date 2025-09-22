from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class EmailStatus(str, Enum):
    draft = "Draft"
    scheduled = "Scheduled"
    sending = "Sending"
    sent = "Sent"
    failed = "Failed"

class EmailTemplateCategory(str, Enum):
    newsletter = "Newsletter"
    promotional = "Promotional"
    transactional = "Transactional"
    welcome = "Welcome"
    abandoned_cart = "Abandoned Cart"
    other = "Other"

class EmailListBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True
    tags: List[str] = []

class EmailListCreate(EmailListBase):
    pass

class EmailListUpdate(EmailListBase):
    pass

class EmailList(EmailListBase):
    id: int
    subscriber_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

class EmailSubscriberBase(BaseModel):
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    list_ids: List[int] = []
    tags: List[str] = []
    is_subscribed: bool = True

class EmailSubscriberCreate(EmailSubscriberBase):
    pass

class EmailSubscriberUpdate(EmailSubscriberBase):
    pass

class EmailSubscriber(EmailSubscriberBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class EmailTemplateBase(BaseModel):
    name: str
    subject: str
    content: str  # HTML content
    category: EmailTemplateCategory = EmailTemplateCategory.newsletter
    is_active: bool = True

class EmailTemplateCreate(EmailTemplateBase):
    pass

class EmailTemplateUpdate(EmailTemplateBase):
    pass

class EmailTemplate(EmailTemplateBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class EmailCampaignBase(BaseModel):
    name: str
    subject: str
    template_id: int
    list_ids: List[int] = []
    status: EmailStatus = EmailStatus.draft
    scheduled_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    tags: List[str] = []

class EmailCampaignCreate(EmailCampaignBase):
    pass

class EmailCampaignUpdate(EmailCampaignBase):
    pass

class EmailCampaign(EmailCampaignBase):
    id: int
    open_rate: float = 0.0
    click_rate: float = 0.0
    bounce_rate: float = 0.0
    unsubscribe_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

class EmailSequenceBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True
    tags: List[str] = []

class EmailSequenceCreate(EmailSequenceBase):
    pass

class EmailSequenceUpdate(EmailSequenceBase):
    pass

class EmailSequence(EmailSequenceBase):
    id: int
    email_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

class EmailSequenceStepBase(BaseModel):
    sequence_id: int
    email_template_id: int
    delay_days: int
    step_order: int

class EmailSequenceStepCreate(EmailSequenceStepBase):
    pass

class EmailSequenceStepUpdate(EmailSequenceStepBase):
    pass

class EmailSequenceStep(EmailSequenceStepBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None