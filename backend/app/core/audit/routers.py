"""
API Routers for Audit Logging Features

This module provides FastAPI endpoints for audit logging operations.
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from .logging import AuditLoggingService, AuditLog
from app.core.database import get_db

# Create routers
audit_router = APIRouter(prefix="/audit", tags=["Audit Logging"])

class AuditLogCreate(BaseModel):
    """Request model for creating audit log entries"""
    organization_id: int
    user_id: Optional[int] = None
    user_email: Optional[str] = None
    action: str
    resource_type: str
    resource_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    details: Optional[dict] = None
    is_sensitive: bool = False

class AuditLogResponse(BaseModel):
    """Response model for audit log entries"""
    id: int
    organization_id: int
    user_id: Optional[int] = None
    user_email: Optional[str] = None
    action: str
    resource_type: str
    resource_id: Optional[str] = None
    timestamp: datetime
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    details: Optional[str] = None
    is_sensitive: bool
    log_hash: str
    is_immutable: bool

    class Config:
        orm_mode = True

class AuditLogQuery(BaseModel):
    """Query model for retrieving audit logs"""
    user_id: Optional[int] = None
    resource_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = 100

class AuditLogIntegrityResponse(BaseModel):
    """Response model for log integrity verification"""
    log_id: int
    is_valid: bool

# Audit Logging Endpoints
@audit_router.post("/logs", response_model=AuditLogResponse)
async def create_audit_log(
    audit_log: AuditLogCreate,
    db: Session = Depends(get_db)
):
    """Create a new audit log entry"""
    audit_service = AuditLoggingService(db)
    try:
        log_entry = audit_service.log_action(
            organization_id=audit_log.organization_id,
            user_id=audit_log.user_id,
            user_email=audit_log.user_email,
            action=audit_log.action,
            resource_type=audit_log.resource_type,
            resource_id=audit_log.resource_id,
            ip_address=audit_log.ip_address,
            user_agent=audit_log.user_agent,
            details=audit_log.details,
            is_sensitive=audit_log.is_sensitive
        )
        return log_entry
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@audit_router.get("/logs/{organization_id}", response_model=List[AuditLogResponse])
async def get_audit_logs(
    organization_id: int,
    query: AuditLogQuery = None,
    db: Session = Depends(get_db)
):
    """Retrieve audit logs for an organization"""
    if query is None:
        query = AuditLogQuery()
    
    audit_service = AuditLoggingService(db)
    logs = audit_service.get_audit_logs(
        organization_id=organization_id,
        user_id=query.user_id,
        resource_type=query.resource_type,
        start_date=query.start_date,
        end_date=query.end_date,
        limit=query.limit
    )
    return logs

@audit_router.post("/logs/{log_id}/verify", response_model=AuditLogIntegrityResponse)
async def verify_log_integrity(
    log_id: int,
    db: Session = Depends(get_db)
):
    """Verify the integrity of an audit log entry"""
    audit_service = AuditLoggingService(db)
    is_valid = audit_service.verify_log_integrity(log_id)
    return AuditLogIntegrityResponse(log_id=log_id, is_valid=is_valid)

@audit_router.get("/logs/{log_id}", response_model=AuditLogResponse)
async def get_audit_log(
    log_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific audit log entry"""
    log_entry = db.query(AuditLog).filter(AuditLog.id == log_id).first()
    if not log_entry:
        raise HTTPException(status_code=404, detail="Audit log not found")
    return log_entry

@audit_router.get("/summary/{organization_id}")
async def get_audit_summary(
    organization_id: int,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get audit log summary for an organization"""
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Get logs in date range
    logs = db.query(AuditLog).filter(
        AuditLog.organization_id == organization_id,
        AuditLog.timestamp >= start_date,
        AuditLog.timestamp <= end_date
    ).all()
    
    # Generate summary statistics
    total_logs = len(logs)
    actions = {}
    resource_types = {}
    users = {}
    
    for log in logs:
        # Count actions
        actions[log.action] = actions.get(log.action, 0) + 1
        
        # Count resource types
        resource_types[log.resource_type] = resource_types.get(log.resource_type, 0) + 1
        
        # Count users
        user_key = log.user_email or log.user_id or "Unknown"
        users[user_key] = users.get(user_key, 0) + 1
    
    return {
        "organization_id": organization_id,
        "period_days": days,
        "total_logs": total_logs,
        "actions_summary": actions,
        "resource_types_summary": resource_types,
        "user_activity_summary": users,
        "date_range": {
            "start": start_date.isoformat(),
            "end": end_date.isoformat()
        }
    }