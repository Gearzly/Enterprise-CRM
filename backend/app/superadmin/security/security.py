from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime
from ..models import Role, RoleCreate, RoleUpdate, Permission, PermissionCreate, PermissionUpdate, Policy, PolicyCreate, PolicyUpdate, User, UserCreate, UserUpdate

router = APIRouter()

# In-memory storage for demo purposes
roles_db = [
    Role(
        id=1,
        organization_id=1,
        name="Admin",
        description="Administrator with full access",
        permissions=["read", "write", "delete", "manage_users"],
        created_at=datetime.now()
    ),
    Role(
        id=2,
        organization_id=1,
        name="Sales Manager",
        description="Manager with sales module access",
        permissions=["read", "write", "manage_sales"],
        created_at=datetime.now()
    )
]

permissions_db = [
    Permission(
        id=1,
        name="Read Access",
        description="Permission to read resources",
        resource="*",
        action="read",
        created_at=datetime.now()
    ),
    Permission(
        id=2,
        name="Write Access",
        description="Permission to create and update resources",
        resource="*",
        action="write",
        created_at=datetime.now()
    )
]

policies_db = [
    Policy(
        id=1,
        organization_id=1,
        name="Work Hours Access",
        description="Access only during work hours",
        effect="allow",
        conditions={"time_range": "9:00-17:00", "weekdays": "mon-fri"},
        created_at=datetime.now()
    )
]

users_db = [
    # Users will be managed through the user service
    # No hardcoded demo users here
]

# Role Management Endpoints
@router.get("/roles", response_model=List[Role])
def list_roles(organization_id: Optional[int] = None):
    """List all roles, optionally filtered by organization"""
    if organization_id:
        return [role for role in roles_db if role.organization_id == organization_id]
    return roles_db

@router.get("/roles/{role_id}", response_model=Role)
def get_role(role_id: int):
    """Get a specific role by ID"""
    for role in roles_db:
        if role.id == role_id:
            return role
    raise HTTPException(status_code=404, detail="Role not found")

@router.post("/roles", response_model=Role)
def create_role(role: RoleCreate):
    """Create a new role"""
    new_id = max([r.id for r in roles_db]) + 1 if roles_db else 1
    new_role = Role(
        id=new_id,
        created_at=datetime.now(),
        **role.dict()
    )
    roles_db.append(new_role)
    return new_role

@router.put("/roles/{role_id}", response_model=Role)
def update_role(role_id: int, role_update: RoleUpdate):
    """Update an existing role"""
    for index, role in enumerate(roles_db):
        if role.id == role_id:
            updated_role = Role(
                id=role_id,
                organization_id=role.organization_id,
                created_at=role.created_at,
                updated_at=datetime.now(),
                **role_update.dict()
            )
            roles_db[index] = updated_role
            return updated_role
    raise HTTPException(status_code=404, detail="Role not found")

@router.delete("/roles/{role_id}")
def delete_role(role_id: int):
    """Delete a role"""
    for index, role in enumerate(roles_db):
        if role.id == role_id:
            del roles_db[index]
            return {"message": "Role deleted successfully"}
    raise HTTPException(status_code=404, detail="Role not found")

# Permission Management Endpoints
@router.get("/permissions", response_model=List[Permission])
def list_permissions():
    """List all permissions"""
    return permissions_db

@router.get("/permissions/{permission_id}", response_model=Permission)
def get_permission(permission_id: int):
    """Get a specific permission by ID"""
    for perm in permissions_db:
        if perm.id == permission_id:
            return perm
    raise HTTPException(status_code=404, detail="Permission not found")

@router.post("/permissions", response_model=Permission)
def create_permission(permission: PermissionCreate):
    """Create a new permission"""
    new_id = max([p.id for p in permissions_db]) + 1 if permissions_db else 1
    new_permission = Permission(
        id=new_id,
        created_at=datetime.now(),
        **permission.dict()
    )
    permissions_db.append(new_permission)
    return new_permission

@router.put("/permissions/{permission_id}", response_model=Permission)
def update_permission(permission_id: int, permission_update: PermissionUpdate):
    """Update an existing permission"""
    for index, perm in enumerate(permissions_db):
        if perm.id == permission_id:
            updated_permission = Permission(
                id=permission_id,
                created_at=perm.created_at,
                **permission_update.dict()
            )
            permissions_db[index] = updated_permission
            return updated_permission
    raise HTTPException(status_code=404, detail="Permission not found")

@router.delete("/permissions/{permission_id}")
def delete_permission(permission_id: int):
    """Delete a permission"""
    for index, perm in enumerate(permissions_db):
        if perm.id == permission_id:
            del permissions_db[index]
            return {"message": "Permission deleted successfully"}
    raise HTTPException(status_code=404, detail="Permission not found")

# Policy Management Endpoints (ABAC)
@router.get("/policies", response_model=List[Policy])
def list_policies(organization_id: Optional[int] = None):
    """List all policies, optionally filtered by organization"""
    if organization_id:
        return [policy for policy in policies_db if policy.organization_id == organization_id]
    return policies_db

@router.get("/policies/{policy_id}", response_model=Policy)
def get_policy(policy_id: int):
    """Get a specific policy by ID"""
    for policy in policies_db:
        if policy.id == policy_id:
            return policy
    raise HTTPException(status_code=404, detail="Policy not found")

@router.post("/policies", response_model=Policy)
def create_policy(policy: PolicyCreate):
    """Create a new policy"""
    new_id = max([p.id for p in policies_db]) + 1 if policies_db else 1
    new_policy = Policy(
        id=new_id,
        created_at=datetime.now(),
        **policy.dict()
    )
    policies_db.append(new_policy)
    return new_policy

@router.put("/policies/{policy_id}", response_model=Policy)
def update_policy(policy_id: int, policy_update: PolicyUpdate):
    """Update an existing policy"""
    for index, policy in enumerate(policies_db):
        if policy.id == policy_id:
            updated_policy = Policy(
                id=policy_id,
                organization_id=policy.organization_id,
                created_at=policy.created_at,
                updated_at=datetime.now(),
                **policy_update.dict()
            )
            policies_db[index] = updated_policy
            return updated_policy
    raise HTTPException(status_code=404, detail="Policy not found")

@router.delete("/policies/{policy_id}")
def delete_policy(policy_id: int):
    """Delete a policy"""
    for index, policy in enumerate(policies_db):
        if policy.id == policy_id:
            del policies_db[index]
            return {"message": "Policy deleted successfully"}
    raise HTTPException(status_code=404, detail="Policy not found")

# User Management Endpoints
@router.get("/users", response_model=List[User])
def list_users(organization_id: Optional[int] = None):
    """List all users, optionally filtered by organization"""
    if organization_id:
        return [user for user in users_db if user.organization_id == organization_id]
    return users_db

@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    """Get a specific user by ID"""
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/users", response_model=User)
def create_user(user: UserCreate):
    """Create a new user"""
    new_id = max([u.id for u in users_db]) + 1 if users_db else 1
    # Get roles by IDs
    user_roles = [role for role in roles_db if role.id in user.role_ids]
    
    new_user = User(
        id=new_id,
        organization_id=1,  # Default for demo
        roles=user_roles,
        created_at=datetime.now(),
        **user.dict(exclude={'role_ids'})
    )
    users_db.append(new_user)
    return new_user

@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserUpdate):
    """Update an existing user"""
    for index, user in enumerate(users_db):
        if user.id == user_id:
            # Get roles by IDs
            user_roles = [role for role in roles_db if role.id in user_update.role_ids]
            
            updated_user = User(
                id=user_id,
                organization_id=user.organization_id,
                roles=user_roles,
                created_at=user.created_at,
                updated_at=datetime.now(),
                **user_update.dict(exclude={'role_ids'})
            )
            users_db[index] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    """Delete a user"""
    for index, user in enumerate(users_db):
        if user.id == user_id:
            del users_db[index]
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")