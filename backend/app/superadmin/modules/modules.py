from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime
from ..models import Module, ModuleCreate, ModuleUpdate, ModuleAssignment, ModuleAssignmentCreate, ModuleAssignmentUpdate

router = APIRouter()

# In-memory storage for demo purposes
modules_db = [
    Module(
        id=1,
        name="Sales",
        description="Sales management module",
        category="core",
        is_active=True,
        required_permissions=["sales.read", "sales.write"],
        created_at=datetime.now()
    ),
    Module(
        id=2,
        name="Marketing",
        description="Marketing automation module",
        category="core",
        is_active=True,
        required_permissions=["marketing.read", "marketing.write"],
        created_at=datetime.now()
    ),
    Module(
        id=3,
        name="Support",
        description="Customer support module",
        category="core",
        is_active=True,
        required_permissions=["support.read", "support.write"],
        created_at=datetime.now()
    ),
    Module(
        id=4,
        name="Analytics",
        description="Business intelligence and reporting",
        category="addon",
        is_active=True,
        required_permissions=["analytics.read"],
        created_at=datetime.now()
    )
]

module_assignments_db = [
    ModuleAssignment(
        id=1,
        organization_id=1,
        module_id=1,
        is_enabled=True,
        config={"max_users": 50, "features": ["leads", "opportunities"]},
        created_at=datetime.now()
    ),
    ModuleAssignment(
        id=2,
        organization_id=1,
        module_id=2,
        is_enabled=True,
        config={"max_users": 30, "features": ["campaigns", "emails"]},
        created_at=datetime.now()
    ),
    ModuleAssignment(
        id=3,
        organization_id=2,
        module_id=1,
        is_enabled=True,
        config={"max_users": 10, "features": ["leads"]},
        created_at=datetime.now()
    )
]

# Module Management Endpoints
@router.get("/", response_model=List[Module])
def list_modules(category: Optional[str] = None):
    """List all modules, optionally filtered by category"""
    if category:
        return [module for module in modules_db if module.category == category]
    return modules_db

@router.get("/{module_id}", response_model=Module)
def get_module(module_id: int):
    """Get a specific module by ID"""
    for module in modules_db:
        if module.id == module_id:
            return module
    raise HTTPException(status_code=404, detail="Module not found")

@router.post("/", response_model=Module)
def create_module(module: ModuleCreate):
    """Create a new module"""
    new_id = max([m.id for m in modules_db]) + 1 if modules_db else 1
    new_module = Module(
        id=new_id,
        created_at=datetime.now(),
        **module.dict()
    )
    modules_db.append(new_module)
    return new_module

@router.put("/{module_id}", response_model=Module)
def update_module(module_id: int, module_update: ModuleUpdate):
    """Update an existing module"""
    for index, module in enumerate(modules_db):
        if module.id == module_id:
            updated_module = Module(
                id=module_id,
                created_at=module.created_at,
                updated_at=datetime.now(),
                **module_update.dict()
            )
            modules_db[index] = updated_module
            return updated_module
    raise HTTPException(status_code=404, detail="Module not found")

@router.delete("/{module_id}")
def delete_module(module_id: int):
    """Delete a module"""
    for index, module in enumerate(modules_db):
        if module.id == module_id:
            del modules_db[index]
            return {"message": "Module deleted successfully"}
    raise HTTPException(status_code=404, detail="Module not found")

# Module Assignment Endpoints
@router.get("/assignments/", response_model=List[ModuleAssignment])
def list_module_assignments(organization_id: Optional[int] = None):
    """List all module assignments, optionally filtered by organization"""
    if organization_id:
        return [assignment for assignment in module_assignments_db if assignment.organization_id == organization_id]
    return module_assignments_db

@router.get("/assignments/{assignment_id}", response_model=ModuleAssignment)
def get_module_assignment(assignment_id: int):
    """Get a specific module assignment by ID"""
    for assignment in module_assignments_db:
        if assignment.id == assignment_id:
            return assignment
    raise HTTPException(status_code=404, detail="Module assignment not found")

@router.post("/assignments/", response_model=ModuleAssignment)
def assign_module_to_organization(assignment: ModuleAssignmentCreate):
    """Assign a module to an organization"""
    new_id = max([a.id for a in module_assignments_db]) + 1 if module_assignments_db else 1
    new_assignment = ModuleAssignment(
        id=new_id,
        created_at=datetime.now(),
        **assignment.dict()
    )
    module_assignments_db.append(new_assignment)
    return new_assignment

@router.put("/assignments/{assignment_id}", response_model=ModuleAssignment)
def update_module_assignment(assignment_id: int, assignment_update: ModuleAssignmentUpdate):
    """Update an existing module assignment"""
    for index, assignment in enumerate(module_assignments_db):
        if assignment.id == assignment_id:
            updated_assignment = ModuleAssignment(
                id=assignment_id,
                organization_id=assignment.organization_id,
                module_id=assignment.module_id,
                created_at=assignment.created_at,
                updated_at=datetime.now(),
                **assignment_update.dict()
            )
            module_assignments_db[index] = updated_assignment
            return updated_assignment
    raise HTTPException(status_code=404, detail="Module assignment not found")

@router.delete("/assignments/{assignment_id}")
def remove_module_assignment(assignment_id: int):
    """Remove a module assignment"""
    for index, assignment in enumerate(module_assignments_db):
        if assignment.id == assignment_id:
            del module_assignments_db[index]
            return {"message": "Module assignment removed successfully"}
    raise HTTPException(status_code=404, detail="Module assignment not found")

@router.post("/assignments/{assignment_id}/enable")
def enable_module_assignment(assignment_id: int):
    """Enable a module assignment"""
    for assignment in module_assignments_db:
        if assignment.id == assignment_id:
            assignment.is_enabled = True
            return {"message": f"Module assignment {assignment_id} enabled successfully"}
    raise HTTPException(status_code=404, detail="Module assignment not found")

@router.post("/assignments/{assignment_id}/disable")
def disable_module_assignment(assignment_id: int):
    """Disable a module assignment"""
    for assignment in module_assignments_db:
        if assignment.id == assignment_id:
            assignment.is_enabled = False
            return {"message": f"Module assignment {assignment_id} disabled successfully"}
    raise HTTPException(status_code=404, detail="Module assignment not found")