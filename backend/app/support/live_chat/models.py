from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
# Removed Enum import since we're removing static enums

# Removed ChatStatus enum
# Removed ChatPriority enum

class ChatSessionBase(BaseModel):
    customer_id: int
    subject: str
    priority: str = "Medium"  # Changed from ChatPriority to str
    assigned_agent_id: Optional[str] = None
    tags: List[str] = []

class ChatSessionCreate(ChatSessionBase):
    pass

class ChatSessionUpdate(ChatSessionBase):
    pass

class ChatSession(ChatSessionBase):
    id: int
    status: str = "Pending"  # Changed from ChatStatus to str
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