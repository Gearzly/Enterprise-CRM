"""
API Routers for Compliance Features

This module provides FastAPI endpoints for GDPR/HIPAA compliance operations.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel
from .gdpr_hipaa import (
    GDPRHIPAAComplianceService,
    DataRetentionPolicy,
    DataRetentionLog,
    DeletionRequest,
    DeletionLog,
    ConsentTemplate,
    ConsentRecord,
    ConsentLog
)
from app.core.database import get_db

# Pydantic models for API requests/responses
class DataRetentionPolicyCreate(BaseModel):
    organization_id: int
    module_name: str
    data_category: str
    retention_period_days: int
    retention_action: str
    description: Optional[str] = None

class DataRetentionPolicyResponse(BaseModel):
    id: int
    organization_id: int
    module_name: str
    data_category: str
    retention_period_days: int
    retention_action: str
    description: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class DeletionRequestCreate(BaseModel):
    organization_id: int
    requester_id: int
    requester_email: str
    target_email: str
    request_type: str
    reason: Optional[str] = None
    data_identifiers: Optional[str] = None  # JSON string

class DeletionRequestResponse(BaseModel):
    id: int
    organization_id: int
    requester_id: int
    requester_email: str
    target_email: str
    request_type: str
    status: str
    reason: Optional[str] = None
    data_identifiers: Optional[str] = None
    requested_at: datetime
    processed_at: Optional[datetime] = None
    processed_by: Optional[str] = None
    rejection_reason: Optional[str] = None

    class Config:
        orm_mode = True

class ConsentTemplateCreate(BaseModel):
    organization_id: int
    name: str
    description: Optional[str] = None
    content: str
    version: str
    required_for: str

class ConsentTemplateResponse(BaseModel):
    id: int
    organization_id: int
    name: str
    description: Optional[str] = None
    content: str
    version: str
    is_active: bool
    required_for: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class ConsentRecordCreate(BaseModel):
    organization_id: int
    user_id: Optional[int] = None
    email: str
    consent_template_id: int
    consent_template_version: str
    status: str = "granted"
    expiry_date: Optional[datetime] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    consent_details: Optional[str] = None  # JSON string

class ConsentRecordResponse(BaseModel):
    id: int
    organization_id: int
    user_id: Optional[int] = None
    email: str
    consent_template_id: int
    consent_template_version: str
    status: str
    granted_at: datetime
    revoked_at: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    consent_details: Optional[str] = None

    class Config:
        orm_mode = True

# Create routers
retention_router = APIRouter(prefix="/retention", tags=["Data Retention"])
deletion_router = APIRouter(prefix="/deletion", tags=["Right to Deletion"])
consent_router = APIRouter(prefix="/consent", tags=["Consent Management"])

# Data Retention Endpoints
@retention_router.post("/policies", response_model=DataRetentionPolicyResponse)
def create_retention_policy(
    policy: DataRetentionPolicyCreate,
    db: Session = Depends(get_db)
):
    """Create a new data retention policy"""
    service = GDPRHIPAAComplianceService(db)
    db_policy = service.create_retention_policy(policy.dict())
    return db_policy

@retention_router.get("/policies/{organization_id}", response_model=List[DataRetentionPolicyResponse])
def list_retention_policies(
    organization_id: int,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """List data retention policies for an organization"""
    service = GDPRHIPAAComplianceService(db)
    policies = service.get_retention_policies(organization_id, active_only)
    return policies

@retention_router.post("/execute/{policy_id}")
def execute_retention_policy(
    policy_id: int,
    executed_by: str = "system",
    db: Session = Depends(get_db)
):
    """Execute a data retention policy"""
    service = GDPRHIPAAComplianceService(db)
    try:
        log_id = service.execute_retention_policy(policy_id, executed_by)
        return {"message": "Retention policy executed successfully", "log_id": log_id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# Right to Deletion Endpoints
@deletion_router.post("/requests", response_model=DeletionRequestResponse)
def create_deletion_request(
    request: DeletionRequestCreate,
    db: Session = Depends(get_db)
):
    """Create a new data deletion request"""
    service = GDPRHIPAAComplianceService(db)
    db_request = service.create_deletion_request(request.dict())
    return db_request

@deletion_router.get("/requests/{organization_id}", response_model=List[DeletionRequestResponse])
def list_deletion_requests(
    organization_id: int,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List data deletion requests for an organization"""
    service = GDPRHIPAAComplianceService(db)
    requests = service.get_deletion_requests(organization_id, status)
    return requests

@deletion_router.post("/process/{request_id}")
def process_deletion_request(
    request_id: int,
    processor: str = "system",
    db: Session = Depends(get_db)
):
    """Process a data deletion request"""
    service = GDPRHIPAAComplianceService(db)
    try:
        success = service.process_deletion_request(request_id, processor)
        return {"message": "Deletion request processed successfully", "success": success}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# Consent Management Endpoints
@consent_router.post("/templates", response_model=ConsentTemplateResponse)
def create_consent_template(
    template: ConsentTemplateCreate,
    db: Session = Depends(get_db)
):
    """Create a new consent template"""
    service = GDPRHIPAAComplianceService(db)
    db_template = service.create_consent_template(template.dict())
    return db_template

@consent_router.get("/templates/{organization_id}", response_model=List[ConsentTemplateResponse])
def list_consent_templates(
    organization_id: int,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """List consent templates for an organization"""
    service = GDPRHIPAAComplianceService(db)
    templates = service.get_consent_templates(organization_id, active_only)
    return templates

@consent_router.post("/records", response_model=ConsentRecordResponse)
def record_consent(
    consent: ConsentRecordCreate,
    db: Session = Depends(get_db)
):
    """Record user consent"""
    service = GDPRHIPAAComplianceService(db)
    db_consent = service.record_consent(consent.dict())
    return db_consent

@consent_router.post("/revoke/{consent_id}")
def revoke_consent(
    consent_id: int,
    revoker: str = "user",
    db: Session = Depends(get_db)
):
    """Revoke user consent"""
    service = GDPRHIPAAComplianceService(db)
    try:
        success = service.revoke_consent(consent_id, revoker)
        return {"message": "Consent revoked successfully", "success": success}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@consent_router.get("/records/{organization_id}/{email}", response_model=List[ConsentRecordResponse])
def get_user_consents(
    organization_id: int,
    email: str,
    db: Session = Depends(get_db)
):
    """Get all consent records for a user"""
    service = GDPRHIPAAComplianceService(db)
    consents = service.get_user_consents(organization_id, email)
    return consents