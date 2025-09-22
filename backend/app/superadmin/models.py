from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

# Organization Models
class OrganizationBase(BaseModel):
    name: str
    domain: Optional[str] = None
    status: str = "active"
    plan_type: str = "basic"
    max_users: int = 10
    features: List[str] = []

class OrganizationCreate(OrganizationBase):
    admin_email: str
    admin_password: str

class OrganizationUpdate(OrganizationBase):
    pass

class Organization(OrganizationBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

# Role Models
class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None
    permissions: List[str] = []

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    pass

class Role(RoleBase):
    id: int
    organization_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

# User Models
class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    status: str = "active"

class UserCreate(UserBase):
    password: str
    role_ids: List[int] = []

class UserUpdate(UserBase):
    role_ids: List[int] = []

class User(UserBase):
    id: int
    organization_id: int
    roles: List[Role] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

# Permission Models
class PermissionBase(BaseModel):
    name: str
    description: Optional[str] = None
    resource: str
    action: str  # read, write, delete, etc.

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(PermissionBase):
    pass

class Permission(PermissionBase):
    id: int
    created_at: datetime

# Policy Models (for ABAC)
class PolicyBase(BaseModel):
    name: str
    description: Optional[str] = None
    effect: str  # allow, deny
    conditions: Dict[str, Any] = {}  # JSON structure for conditions

class PolicyCreate(PolicyBase):
    pass

class PolicyUpdate(PolicyBase):
    pass

class Policy(PolicyBase):
    id: int
    organization_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

# Module Models
class ModuleBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    is_active: bool = True
    required_permissions: List[str] = []

class ModuleCreate(ModuleBase):
    pass

class ModuleUpdate(ModuleBase):
    pass

class Module(ModuleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

# Module Assignment Models
class ModuleAssignmentBase(BaseModel):
    organization_id: int
    module_id: int
    is_enabled: bool = True
    config: Dict[str, Any] = {}

class ModuleAssignmentCreate(ModuleAssignmentBase):
    pass

class ModuleAssignmentUpdate(ModuleAssignmentBase):
    pass

class ModuleAssignment(ModuleAssignmentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

# Settings Models
class SystemSettingBase(BaseModel):
    key: str
    value: str
    description: Optional[str] = None
    category: str

class SystemSettingCreate(SystemSettingBase):
    pass

class SystemSettingUpdate(SystemSettingBase):
    pass

class SystemSetting(SystemSettingBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

# Sales Configuration Models
class SalesConfigBase(BaseModel):
    key: str
    value: str
    description: Optional[str] = None
    category: str
    organization_id: Optional[int] = None  # None for global, specific ID for org-specific

class SalesConfigCreate(SalesConfigBase):
    pass

class SalesConfigUpdate(SalesConfigBase):
    pass

class SalesConfig(SalesConfigBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

# Marketing Configuration Models
class MarketingConfigBase(BaseModel):
    key: str
    value: str
    description: Optional[str] = None
    category: str
    organization_id: Optional[int] = None  # None for global, specific ID for org-specific

class MarketingConfigCreate(MarketingConfigBase):
    pass

class MarketingConfigUpdate(MarketingConfigBase):
    pass

class MarketingConfig(MarketingConfigBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None