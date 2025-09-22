from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime
from ..models import SystemSetting, SystemSettingCreate, SystemSettingUpdate

router = APIRouter()

# In-memory storage for demo purposes
settings_db = [
    SystemSetting(
        id=1,
        key="email_provider",
        value="smtp",
        description="Email service provider",
        category="email",
        created_at=datetime.now()
    ),
    SystemSetting(
        id=2,
        key="max_file_upload_size",
        value="10MB",
        description="Maximum file upload size",
        category="system",
        created_at=datetime.now()
    ),
    SystemSetting(
        id=3,
        key="data_retention_period",
        value="365",
        description="Data retention period in days",
        category="data",
        created_at=datetime.now()
    )
]

@router.get("/", response_model=List[SystemSetting])
def list_settings(category: Optional[str] = None):
    """List all system settings, optionally filtered by category"""
    if category:
        return [setting for setting in settings_db if setting.category == category]
    return settings_db

@router.get("/{setting_id}", response_model=SystemSetting)
def get_setting(setting_id: int):
    """Get a specific system setting by ID"""
    for setting in settings_db:
        if setting.id == setting_id:
            return setting
    raise HTTPException(status_code=404, detail="Setting not found")

@router.post("/", response_model=SystemSetting)
def create_setting(setting: SystemSettingCreate):
    """Create a new system setting"""
    new_id = max([s.id for s in settings_db]) + 1 if settings_db else 1
    new_setting = SystemSetting(
        id=new_id,
        created_at=datetime.now(),
        **setting.dict()
    )
    settings_db.append(new_setting)
    return new_setting

@router.put("/{setting_id}", response_model=SystemSetting)
def update_setting(setting_id: int, setting_update: SystemSettingUpdate):
    """Update an existing system setting"""
    for index, setting in enumerate(settings_db):
        if setting.id == setting_id:
            updated_setting = SystemSetting(
                id=setting_id,
                created_at=setting.created_at,
                updated_at=datetime.now(),
                **setting_update.dict()
            )
            settings_db[index] = updated_setting
            return updated_setting
    raise HTTPException(status_code=404, detail="Setting not found")

@router.delete("/{setting_id}")
def delete_setting(setting_id: int):
    """Delete a system setting"""
    for index, setting in enumerate(settings_db):
        if setting.id == setting_id:
            del settings_db[index]
            return {"message": "Setting deleted successfully"}
    raise HTTPException(status_code=404, detail="Setting not found")

@router.get("/categories", response_model=List[str])
def list_categories():
    """List all setting categories"""
    categories = list(set([setting.category for setting in settings_db]))
    return categories

@router.get("/search/", response_model=List[SystemSetting])
def search_settings(key: Optional[str] = None):
    """Search settings by key"""
    if key:
        return [setting for setting in settings_db if key.lower() in setting.key.lower()]
    return settings_db