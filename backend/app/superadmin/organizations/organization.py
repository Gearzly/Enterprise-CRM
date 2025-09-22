from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from ..models import Organization, OrganizationCreate, OrganizationUpdate

router = APIRouter()

# In-memory storage for demo purposes
organizations_db = [
    Organization(
        id=1,
        name="Acme Corporation",
        domain="acme.crm.com",
        status="active",
        plan_type="enterprise",
        max_users=100,
        features=["sales", "marketing", "support"],
        created_at=datetime.now()
    ),
    Organization(
        id=2,
        name="Beta Startup",
        domain="beta.crm.com",
        status="active",
        plan_type="professional",
        max_users=25,
        features=["sales"],
        created_at=datetime.now()
    )
]

@router.get("/", response_model=List[Organization])
def list_organizations():
    """List all organizations"""
    return organizations_db

@router.get("/{org_id}", response_model=Organization)
def get_organization(org_id: int):
    """Get a specific organization by ID"""
    for org in organizations_db:
        if org.id == org_id:
            return org
    raise HTTPException(status_code=404, detail="Organization not found")

@router.post("/", response_model=Organization)
def create_organization(organization: OrganizationCreate):
    """Create a new organization"""
    new_id = max([org.id for org in organizations_db]) + 1 if organizations_db else 1
    new_org = Organization(
        id=new_id,
        created_at=datetime.now(),
        **organization.dict()
    )
    organizations_db.append(new_org)
    return new_org

@router.put("/{org_id}", response_model=Organization)
def update_organization(org_id: int, organization_update: OrganizationUpdate):
    """Update an existing organization"""
    for index, org in enumerate(organizations_db):
        if org.id == org_id:
            updated_org = Organization(
                id=org_id,
                created_at=org.created_at,
                updated_at=datetime.now(),
                **organization_update.dict()
            )
            organizations_db[index] = updated_org
            return updated_org
    raise HTTPException(status_code=404, detail="Organization not found")

@router.delete("/{org_id}")
def delete_organization(org_id: int):
    """Delete an organization"""
    for index, org in enumerate(organizations_db):
        if org.id == org_id:
            del organizations_db[index]
            return {"message": "Organization deleted successfully"}
    raise HTTPException(status_code=404, detail="Organization not found")

@router.post("/{org_id}/suspend")
def suspend_organization(org_id: int):
    """Suspend an organization"""
    for org in organizations_db:
        if org.id == org_id:
            org.status = "suspended"
            return {"message": f"Organization {org_id} suspended successfully"}
    raise HTTPException(status_code=404, detail="Organization not found")

@router.post("/{org_id}/activate")
def activate_organization(org_id: int):
    """Activate a suspended organization"""
    for org in organizations_db:
        if org.id == org_id:
            org.status = "active"
            return {"message": f"Organization {org_id} activated successfully"}
    raise HTTPException(status_code=404, detail="Organization not found")