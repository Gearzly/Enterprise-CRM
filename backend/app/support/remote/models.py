from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
# Removed Enum import since we're removing static enums

# Removed RemoteSessionStatus enum
# Removed RemoteSessionType enum
# Removed RemotePlatform enum

class RemoteSessionBase(BaseModel):
    customer_id: int
    agent_id: str
    session_type: str  # Changed from RemoteSessionType to str
    platform: str  # Changed from RemotePlatform to str
    device_info: Optional[str] = None
    purpose: Optional[str] = None
    tags: List[str] = []

class RemoteSessionCreate(RemoteSessionBase):
    pass

class RemoteSessionUpdate(RemoteSessionBase):
    pass

class RemoteSession(RemoteSessionBase):
    id: int
    status: str = "Pending"  # Changed from RemoteSessionStatus to str
    created_at: datetime
    updated_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None

class DiagnosticToolBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    command: str
    is_active: bool = True

class DiagnosticToolCreate(DiagnosticToolBase):
    pass

class DiagnosticToolUpdate(DiagnosticToolBase):
    pass

class DiagnosticTool(DiagnosticToolBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class DiagnosticResultBase(BaseModel):
    session_id: int
    tool_id: int
    output: str
    success: bool = True

class DiagnosticResultCreate(DiagnosticResultBase):
    pass

class DiagnosticResult(DiagnosticResultBase):
    id: int
    created_at: datetime

class FileTransferBase(BaseModel):
    session_id: int
    file_name: str
    file_size: int
    direction: str  # upload or download
    success: bool = True

class FileTransferCreate(FileTransferBase):
    pass

class FileTransfer(FileTransferBase):
    id: int
    created_at: datetime