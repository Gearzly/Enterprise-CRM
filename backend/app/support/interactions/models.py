from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class InteractionType(str, Enum):
    call = "Call"
    email = "Email"
    chat = "Chat"
    meeting = "Meeting"
    note = "Note"
    follow_up = "Follow Up"

class InteractionBase(BaseModel):
    customer_id: int
    type: InteractionType
    subject: str
    description: Optional[str] = None
    agent_id: Optional[str] = None
    tags: List[str] = []

class InteractionCreate(InteractionBase):
    pass

class InteractionUpdate(InteractionBase):
    pass

class Interaction(InteractionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class InteractionNoteBase(BaseModel):
    interaction_id: int
    content: str
    created_by: str

class InteractionNoteCreate(InteractionNoteBase):
    pass

class InteractionNote(InteractionNoteBase):
    id: int
    created_at: datetime