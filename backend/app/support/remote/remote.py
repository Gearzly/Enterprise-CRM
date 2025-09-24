from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .models import (
    RemoteSession, RemoteSessionCreate, RemoteSessionUpdate,
    DiagnosticTool, DiagnosticToolCreate, DiagnosticToolUpdate,
    DiagnosticResult, DiagnosticResultCreate,
    FileTransfer, FileTransferCreate
)
from .config import (
    get_remote_session_types, get_remote_platforms, get_remote_session_statuses,
    get_default_session_type, get_default_platform, get_max_file_transfer_size_mb
)

router = APIRouter(prefix="/remote", tags=["remote"])

# In-memory storage for demo purposes
remote_sessions_db = []
diagnostic_tools_db = []
diagnostic_results_db = []
file_transfers_db = []

@router.get("/")
def get_remote_support_dashboard():
    """Get remote support dashboard with summary statistics"""
    return {
        "message": "Support Remote Dashboard",
        "statistics": {
            "total_sessions": len(remote_sessions_db),
            "active_sessions": len([s for s in remote_sessions_db if s.status == "Active"]),
            "diagnostic_tools": len(diagnostic_tools_db),
            "file_transfers": len(file_transfers_db)
        }
    }

@router.get("/sessions", response_model=List[RemoteSession])
def list_remote_sessions():
    """List all remote sessions"""
    return remote_sessions_db

@router.get("/sessions/{session_id}", response_model=RemoteSession)
def get_remote_session(session_id: int):
    """Get a specific remote session by ID"""
    for session in remote_sessions_db:
        if session.id == session_id:
            return session
    raise HTTPException(status_code=404, detail="Remote session not found")

@router.post("/sessions", response_model=RemoteSession)
def create_remote_session(session: RemoteSessionCreate):
    """Create a new remote session"""
    new_id = max([s.id for s in remote_sessions_db]) + 1 if remote_sessions_db else 1
    new_session = RemoteSession(
        id=new_id,
        created_at=datetime.now(),
        **session.dict()
    )
    remote_sessions_db.append(new_session)
    return new_session

@router.put("/sessions/{session_id}", response_model=RemoteSession)
def update_remote_session(session_id: int, session_update: RemoteSessionUpdate):
    """Update an existing remote session"""
    for index, session in enumerate(remote_sessions_db):
        if session.id == session_id:
            updated_session = RemoteSession(
                id=session_id,
                created_at=session.created_at,
                updated_at=datetime.now(),
                **session_update.dict()
            )
            remote_sessions_db[index] = updated_session
            return updated_session
    raise HTTPException(status_code=404, detail="Remote session not found")

@router.delete("/sessions/{session_id}")
def delete_remote_session(session_id: int):
    """Delete a remote session"""
    for index, session in enumerate(remote_sessions_db):
        if session.id == session_id:
            del remote_sessions_db[index]
            return {"message": "Remote session deleted successfully"}
    raise HTTPException(status_code=404, detail="Remote session not found")

@router.post("/sessions/{session_id}/start")
def start_remote_session(session_id: int):
    """Start a remote session"""
    for index, session in enumerate(remote_sessions_db):
        if session.id == session_id:
            remote_sessions_db[index].status = "Active"
            remote_sessions_db[index].started_at = datetime.now()
            return {"message": "Remote session started successfully"}
    raise HTTPException(status_code=404, detail="Remote session not found")

@router.post("/sessions/{session_id}/end")
def end_remote_session(session_id: int, duration_seconds: Optional[int] = None):
    """End a remote session"""
    for index, session in enumerate(remote_sessions_db):
        if session.id == session_id:
            remote_sessions_db[index].status = "Completed"
            remote_sessions_db[index].ended_at = datetime.now()
            if duration_seconds is not None:
                remote_sessions_db[index].duration_seconds = duration_seconds
            return {"message": "Remote session ended successfully"}
    raise HTTPException(status_code=404, detail="Remote session not found")

@router.post("/sessions/{session_id}/cancel")
def cancel_remote_session(session_id: int):
    """Cancel a remote session"""
    for index, session in enumerate(remote_sessions_db):
        if session.id == session_id:
            remote_sessions_db[index].status = "Cancelled"
            return {"message": "Remote session cancelled successfully"}
    raise HTTPException(status_code=404, detail="Remote session not found")

@router.get("/sessions/customer/{customer_id}", response_model=List[RemoteSession])
def get_remote_sessions_by_customer(customer_id: int):
    """Get remote sessions by customer ID"""
    return [session for session in remote_sessions_db if session.customer_id == customer_id]

@router.get("/sessions/agent/{agent_id}", response_model=List[RemoteSession])
def get_remote_sessions_by_agent(agent_id: str):
    """Get remote sessions by agent ID"""
    return [session for session in remote_sessions_db if session.agent_id == agent_id]

@router.get("/sessions/status/{status}", response_model=List[RemoteSession])
def get_remote_sessions_by_status(status: str):
    """Get remote sessions by status"""
    # Normalize the status parameter to handle case differences
    normalized_status = status.lower().title()
    return [session for session in remote_sessions_db if session.status == normalized_status]

@router.get("/sessions/platform/{platform}", response_model=List[RemoteSession])
def get_remote_sessions_by_platform(platform: str):
    """Get remote sessions by platform"""
    # Normalize the platform parameter to handle case differences
    normalized_platform = platform.lower().title()
    return [session for session in remote_sessions_db if session.platform == normalized_platform]

# Diagnostic Tool endpoints
@router.get("/tools", response_model=List[DiagnosticTool])
def list_diagnostic_tools():
    """List all diagnostic tools"""
    return diagnostic_tools_db

@router.get("/tools/{tool_id}", response_model=DiagnosticTool)
def get_diagnostic_tool(tool_id: int):
    """Get a specific diagnostic tool by ID"""
    for tool in diagnostic_tools_db:
        if tool.id == tool_id:
            return tool
    raise HTTPException(status_code=404, detail="Diagnostic tool not found")

@router.post("/tools", response_model=DiagnosticTool)
def create_diagnostic_tool(tool: DiagnosticToolCreate):
    """Create a new diagnostic tool"""
    new_id = max([t.id for t in diagnostic_tools_db]) + 1 if diagnostic_tools_db else 1
    new_tool = DiagnosticTool(
        id=new_id,
        created_at=datetime.now(),
        **tool.dict()
    )
    diagnostic_tools_db.append(new_tool)
    return new_tool

@router.put("/tools/{tool_id}", response_model=DiagnosticTool)
def update_diagnostic_tool(tool_id: int, tool_update: DiagnosticToolUpdate):
    """Update an existing diagnostic tool"""
    for index, tool in enumerate(diagnostic_tools_db):
        if tool.id == tool_id:
            updated_tool = DiagnosticTool(
                id=tool_id,
                created_at=tool.created_at,
                updated_at=datetime.now(),
                **tool_update.dict()
            )
            diagnostic_tools_db[index] = updated_tool
            return updated_tool
    raise HTTPException(status_code=404, detail="Diagnostic tool not found")

@router.delete("/tools/{tool_id}")
def delete_diagnostic_tool(tool_id: int):
    """Delete a diagnostic tool"""
    for index, tool in enumerate(diagnostic_tools_db):
        if tool.id == tool_id:
            del diagnostic_tools_db[index]
            return {"message": "Diagnostic tool deleted successfully"}
    raise HTTPException(status_code=404, detail="Diagnostic tool not found")

@router.post("/tools/{tool_id}/activate")
def activate_diagnostic_tool(tool_id: int):
    """Activate a diagnostic tool"""
    for index, tool in enumerate(diagnostic_tools_db):
        if tool.id == tool_id:
            diagnostic_tools_db[index].is_active = True
            return {"message": "Diagnostic tool activated successfully"}
    raise HTTPException(status_code=404, detail="Diagnostic tool not found")

@router.post("/tools/{tool_id}/deactivate")
def deactivate_diagnostic_tool(tool_id: int):
    """Deactivate a diagnostic tool"""
    for index, tool in enumerate(diagnostic_tools_db):
        if tool.id == tool_id:
            diagnostic_tools_db[index].is_active = False
            return {"message": "Diagnostic tool deactivated successfully"}
    raise HTTPException(status_code=404, detail="Diagnostic tool not found")

@router.get("/tools/category/{category}", response_model=List[DiagnosticTool])
def get_diagnostic_tools_by_category(category: str):
    """Get diagnostic tools by category"""
    return [tool for tool in diagnostic_tools_db if tool.category == category]

# Diagnostic Result endpoints
@router.get("/results", response_model=List[DiagnosticResult])
def list_diagnostic_results():
    """List all diagnostic results"""
    return diagnostic_results_db

@router.get("/results/{result_id}", response_model=DiagnosticResult)
def get_diagnostic_result(result_id: int):
    """Get a specific diagnostic result by ID"""
    for result in diagnostic_results_db:
        if result.id == result_id:
            return result
    raise HTTPException(status_code=404, detail="Diagnostic result not found")

@router.post("/results", response_model=DiagnosticResult)
def create_diagnostic_result(result: DiagnosticResultCreate):
    """Create a new diagnostic result"""
    new_id = max([r.id for r in diagnostic_results_db]) + 1 if diagnostic_results_db else 1
    new_result = DiagnosticResult(
        id=new_id,
        created_at=datetime.now(),
        **result.dict()
    )
    diagnostic_results_db.append(new_result)
    return new_result

@router.get("/sessions/{session_id}/results", response_model=List[DiagnosticResult])
def get_results_for_session(session_id: int):
    """Get diagnostic results for a specific session"""
    return [result for result in diagnostic_results_db if result.session_id == session_id]

@router.get("/tools/{tool_id}/results", response_model=List[DiagnosticResult])
def get_results_for_tool(tool_id: int):
    """Get diagnostic results for a specific tool"""
    return [result for result in diagnostic_results_db if result.tool_id == tool_id]

# File Transfer endpoints
@router.get("/transfers", response_model=List[FileTransfer])
def list_file_transfers():
    """List all file transfers"""
    return file_transfers_db

@router.get("/transfers/{transfer_id}", response_model=FileTransfer)
def get_file_transfer(transfer_id: int):
    """Get a specific file transfer by ID"""
    for transfer in file_transfers_db:
        if transfer.id == transfer_id:
            return transfer
    raise HTTPException(status_code=404, detail="File transfer not found")

@router.post("/transfers", response_model=FileTransfer)
def create_file_transfer(transfer: FileTransferCreate):
    """Create a new file transfer"""
    new_id = max([t.id for t in file_transfers_db]) + 1 if file_transfers_db else 1
    new_transfer = FileTransfer(
        id=new_id,
        created_at=datetime.now(),
        **transfer.dict()
    )
    file_transfers_db.append(new_transfer)
    return new_transfer

@router.get("/sessions/{session_id}/transfers", response_model=List[FileTransfer])
def get_transfers_for_session(session_id: int):
    """Get file transfers for a specific session"""
    return [transfer for transfer in file_transfers_db if transfer.session_id == session_id]

@router.get("/transfers/failed", response_model=List[FileTransfer])
def get_failed_file_transfers():
    """Get all failed file transfers"""
    return [transfer for transfer in file_transfers_db if not transfer.success]

# Configuration endpoints
@router.get("/config/session-types", response_model=List[str])
def get_remote_session_type_options():
    """Get available remote session type options"""
    return get_remote_session_types()

@router.get("/config/platforms", response_model=List[str])
def get_remote_platform_options():
    """Get available remote platform options"""
    return get_remote_platforms()

@router.get("/config/statuses", response_model=List[str])
def get_remote_session_status_options():
    """Get available remote session status options"""
    return get_remote_session_statuses()

@router.get("/config/max-file-size", response_model=int)
def get_max_file_transfer_size():
    """Get maximum file transfer size in MB"""
    return get_max_file_transfer_size_mb()