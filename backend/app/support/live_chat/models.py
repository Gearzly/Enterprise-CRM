from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class ChatStatus(str, Enum):
    pending = "Pending"
    active = "Active"
    closed = "Closed"
    transferred = "Transferred"

class ChatPriority(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"

class ChatSessionBase(BaseModel):
    customer_id: int
    subject: str
    priority: ChatPriority = ChatPriority.medium
    assigned_agent_id: Optional[str] = None
    tags: List[str] = []

class ChatSessionCreate(ChatSessionBase):
    pass

class ChatSessionUpdate(ChatSessionBase):
    pass

class ChatSession(ChatSessionBase):
    id: int
    status: ChatStatus = ChatStatus.pending
    created_at: datetime
    updated_at: Optional[datetime] = None
    accepted_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None

class ChatMessageBase(BaseModel):
    session_id: int
    sender_id: str  # Could be customer ID or agent ID
    sender_type: str  # "customer" or "agent"
    content: str

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessage(ChatMessageBase):
    id: int
    timestamp: datetime
    is_read: bool = False

class ChatTranscriptBase(BaseModel):
    session_id: int
    content: str

class ChatTranscriptCreate(ChatTranscriptBase):
    pass

class ChatTranscript(ChatTranscriptBase):
    id: int
    created_at: datetime