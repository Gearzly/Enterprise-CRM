"""
API Routers for Data Classification Features

This module provides FastAPI endpoints for data classification operations.
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from .classification import (
    DataClassificationService,
    DataClassification,
    DataLabel,
    DATA_CLASSIFICATION_TEMPLATES,
    get_classification_requirements,
    check_data_access_permission
)
from app.core.database import get_db

# Create routers
classification_router = APIRouter(prefix="/classification", tags=["Data Classification"])

class DataClassificationCreate(BaseModel):
    """Request model for creating data classifications"""
    organization_id: int
    name: str
    description: Optional[str] = None
    classification_level: str
    data_patterns: str  # JSON string
    handling_procedures: str  # JSON string
    retention_period_days: int
    encryption_required: bool = False
    access_control_required: bool = False
    audit_logging_required: bool = False

class DataClassificationResponse(BaseModel):
    """Response model for data classifications"""
    id: int
    organization_id: int
    name: str
    description: Optional[str] = None
    classification_level: str
    data_patterns: str
    handling_procedures: str
    retention_period_days: int
    encryption_required: bool
    access_control_required: bool
    audit_logging_required: bool

    class Config:
        orm_mode = True

class DataLabelCreate(BaseModel):
    """Request model for labeling data"""
    organization_id: int
    data_type: str
    data_id: str
    data_content: str
    labeled_by: str

class DataLabelResponse(BaseModel):
    """Response model for data labels"""
    id: int
    organization_id: int
    data_type: str
    data_id: str
    classification_id: Optional[int] = None
    classification_level: str
    labeled_at: str
    labeled_by: str
    is_active: bool

    class Config:
        orm_mode = True

class ClassificationRequirementsResponse(BaseModel):
    """Response model for classification requirements"""
    classification_level: str
    requirements: dict

class AccessPermissionRequest(BaseModel):
    """Request model for checking access permissions"""
    user_classification_level: str
    data_classification_level: str

class AccessPermissionResponse(BaseModel):
    """Response model for access permission check"""
    user_classification_level: str
    data_classification_level: str
    has_permission: bool

# Data Classification Endpoints
@classification_router.post("/classifications", response_model=DataClassificationResponse)
async def create_classification(
    classification: DataClassificationCreate,
    db: Session = Depends(get_db)
):
    """Create a new data classification policy"""
    classification_service = DataClassificationService(db)
    try:
        db_classification = classification_service.create_classification(classification.dict())
        return db_classification
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@classification_router.get("/classifications/{organization_id}", response_model=List[DataClassificationResponse])
async def get_classifications(
    organization_id: int,
    db: Session = Depends(get_db)
):
    """Get all data classifications for an organization"""
    classification_service = DataClassificationService(db)
    classifications = classification_service.get_classifications(organization_id)
    return classifications

@classification_router.post("/labels", response_model=DataLabelResponse)
async def classify_data(
    label: DataLabelCreate,
    db: Session = Depends(get_db)
):
    """Classify a data instance"""
    classification_service = DataClassificationService(db)
    try:
        db_label = classification_service.classify_data(
            organization_id=label.organization_id,
            data_type=label.data_type,
            data_id=label.data_id,
            data_content=label.data_content,
            labeled_by=label.labeled_by
        )
        return db_label
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@classification_router.get("/labels/{organization_id}", response_model=List[DataLabelResponse])
async def get_data_labels(
    organization_id: int,
    data_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get data labels for an organization"""
    classification_service = DataClassificationService(db)
    labels = classification_service.get_data_labels(organization_id, data_type)
    return labels

@classification_router.get("/requirements/{classification_level}", response_model=ClassificationRequirementsResponse)
async def get_classification_requirements_endpoint(
    classification_level: str
):
    """Get security requirements for a classification level"""
    try:
        requirements = get_classification_requirements(classification_level)
        return ClassificationRequirementsResponse(
            classification_level=classification_level,
            requirements=requirements
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@classification_router.post("/access-check", response_model=AccessPermissionResponse)
async def check_access_permission(
    request: AccessPermissionRequest
):
    """Check if a user has permission to access data based on classification levels"""
    has_permission = check_data_access_permission(
        request.user_classification_level,
        request.data_classification_level
    )
    return AccessPermissionResponse(
        user_classification_level=request.user_classification_level,
        data_classification_level=request.data_classification_level,
        has_permission=has_permission
    )

@classification_router.get("/templates")
async def get_classification_templates():
    """Get predefined data classification templates"""
    return DATA_CLASSIFICATION_TEMPLATES

@classification_router.get("/levels")
async def get_classification_levels():
    """Get available data classification levels"""
    from .classification import DataClassificationLevel
    return {
        "levels": [level.value for level in DataClassificationLevel]
    }