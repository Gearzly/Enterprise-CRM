from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from .models import (
    AutomationRule, AutomationRuleCreate, AutomationRuleUpdate,
    Workflow, WorkflowCreate, WorkflowUpdate,
    WorkflowStep, WorkflowStepCreate, WorkflowStepUpdate,
    ScheduledTask, ScheduledTaskCreate, ScheduledTaskUpdate
)
from .config import (
    get_automation_types, get_trigger_types, get_action_types,
    get_default_automation_type, get_default_trigger_type, get_max_conditions_per_rule
)

router = APIRouter()

# In-memory storage for demo purposes
automation_rules_db = []
workflows_db = []
workflow_steps_db = []
scheduled_tasks_db = []

@router.get("/rules", response_model=List[AutomationRule])
def list_automation_rules():
    """List all automation rules"""
    return automation_rules_db

@router.get("/rules/{rule_id}", response_model=AutomationRule)
def get_automation_rule(rule_id: int):
    """Get a specific automation rule by ID"""
    for rule in automation_rules_db:
        if rule.id == rule_id:
            return rule
    raise HTTPException(status_code=404, detail="Automation rule not found")

@router.post("/rules", response_model=AutomationRule)
def create_automation_rule(rule: AutomationRuleCreate):
    """Create a new automation rule"""
    new_id = max([r.id for r in automation_rules_db]) + 1 if automation_rules_db else 1
    new_rule = AutomationRule(
        id=new_id,
        created_at=datetime.now(),
        **rule.dict()
    )
    automation_rules_db.append(new_rule)
    return new_rule

@router.put("/rules/{rule_id}", response_model=AutomationRule)
def update_automation_rule(rule_id: int, rule_update: AutomationRuleUpdate):
    """Update an existing automation rule"""
    for index, rule in enumerate(automation_rules_db):
        if rule.id == rule_id:
            updated_rule = AutomationRule(
                id=rule_id,
                created_at=rule.created_at,
                updated_at=datetime.now(),
                **rule_update.dict()
            )
            automation_rules_db[index] = updated_rule
            return updated_rule
    raise HTTPException(status_code=404, detail="Automation rule not found")

@router.delete("/rules/{rule_id}")
def delete_automation_rule(rule_id: int):
    """Delete an automation rule"""
    for index, rule in enumerate(automation_rules_db):
        if rule.id == rule_id:
            del automation_rules_db[index]
            return {"message": "Automation rule deleted successfully"}
    raise HTTPException(status_code=404, detail="Automation rule not found")

@router.post("/rules/{rule_id}/activate")
def activate_automation_rule(rule_id: int):
    """Activate an automation rule"""
    for index, rule in enumerate(automation_rules_db):
        if rule.id == rule_id:
            automation_rules_db[index].is_active = True
            automation_rules_db[index].status = "Active"
            return {"message": "Automation rule activated successfully"}
    raise HTTPException(status_code=404, detail="Automation rule not found")

@router.post("/rules/{rule_id}/deactivate")
def deactivate_automation_rule(rule_id: int):
    """Deactivate an automation rule"""
    for index, rule in enumerate(automation_rules_db):
        if rule.id == rule_id:
            automation_rules_db[index].is_active = False
            automation_rules_db[index].status = "Inactive"
            return {"message": "Automation rule deactivated successfully"}
    raise HTTPException(status_code=404, detail="Automation rule not found")

@router.post("/rules/{rule_id}/pause")
def pause_automation_rule(rule_id: int):
    """Pause an automation rule"""
    for index, rule in enumerate(automation_rules_db):
        if rule.id == rule_id:
            automation_rules_db[index].status = "Paused"
            return {"message": "Automation rule paused successfully"}
    raise HTTPException(status_code=404, detail="Automation rule not found")

@router.get("/rules/type/{type}", response_model=List[AutomationRule])
def get_rules_by_type(type: str):
    """Get automation rules by type"""
    # Normalize the type parameter to handle case differences
    normalized_type = type.lower().title()
    return [rule for rule in automation_rules_db if rule.type.value == normalized_type]

@router.get("/rules/status/{status}", response_model=List[AutomationRule])
def get_rules_by_status(status: str):
    """Get automation rules by status"""
    # Normalize the status parameter to handle case differences
    normalized_status = status.lower().title()
    return [rule for rule in automation_rules_db if rule.status.value == normalized_status]

@router.post("/rules/{rule_id}/trigger")
def trigger_automation_rule(rule_id: int):
    """Manually trigger an automation rule"""
    for index, rule in enumerate(automation_rules_db):
        if rule.id == rule_id:
            automation_rules_db[index].last_triggered_at = datetime.now()
            automation_rules_db[index].trigger_count += 1
            # In a real implementation, this would execute the rule's actions
            return {"message": "Automation rule triggered successfully"}
    raise HTTPException(status_code=404, detail="Automation rule not found")

# Workflow endpoints
@router.get("/workflows", response_model=List[Workflow])
def list_workflows():
    """List all workflows"""
    return workflows_db

@router.get("/workflows/{workflow_id}", response_model=Workflow)
def get_workflow(workflow_id: int):
    """Get a specific workflow by ID"""
    for workflow in workflows_db:
        if workflow.id == workflow_id:
            return workflow
    raise HTTPException(status_code=404, detail="Workflow not found")

@router.post("/workflows", response_model=Workflow)
def create_workflow(workflow: WorkflowCreate):
    """Create a new workflow"""
    new_id = max([w.id for w in workflows_db]) + 1 if workflows_db else 1
    new_workflow = Workflow(
        id=new_id,
        created_at=datetime.now(),
        **workflow.dict()
    )
    workflows_db.append(new_workflow)
    return new_workflow

@router.put("/workflows/{workflow_id}", response_model=Workflow)
def update_workflow(workflow_id: int, workflow_update: WorkflowUpdate):
    """Update an existing workflow"""
    for index, workflow in enumerate(workflows_db):
        if workflow.id == workflow_id:
            updated_workflow = Workflow(
                id=workflow_id,
                created_at=workflow.created_at,
                updated_at=datetime.now(),
                **workflow_update.dict()
            )
            workflows_db[index] = updated_workflow
            return updated_workflow
    raise HTTPException(status_code=404, detail="Workflow not found")

@router.delete("/workflows/{workflow_id}")
def delete_workflow(workflow_id: int):
    """Delete a workflow"""
    for index, workflow in enumerate(workflows_db):
        if workflow.id == workflow_id:
            del workflows_db[index]
            return {"message": "Workflow deleted successfully"}
    raise HTTPException(status_code=404, detail="Workflow not found")

@router.post("/workflows/{workflow_id}/activate")
def activate_workflow(workflow_id: int):
    """Activate a workflow"""
    for index, workflow in enumerate(workflows_db):
        if workflow.id == workflow_id:
            workflows_db[index].is_active = True
            return {"message": "Workflow activated successfully"}
    raise HTTPException(status_code=404, detail="Workflow not found")

@router.post("/workflows/{workflow_id}/deactivate")
def deactivate_workflow(workflow_id: int):
    """Deactivate a workflow"""
    for index, workflow in enumerate(workflows_db):
        if workflow.id == workflow_id:
            workflows_db[index].is_active = False
            return {"message": "Workflow deactivated successfully"}
    raise HTTPException(status_code=404, detail="Workflow not found")

# Workflow Step endpoints
@router.get("/steps", response_model=List[WorkflowStep])
def list_workflow_steps():
    """List all workflow steps"""
    return workflow_steps_db

@router.get("/steps/{step_id}", response_model=WorkflowStep)
def get_workflow_step(step_id: int):
    """Get a specific workflow step by ID"""
    for step in workflow_steps_db:
        if step.id == step_id:
            return step
    raise HTTPException(status_code=404, detail="Workflow step not found")

@router.post("/steps", response_model=WorkflowStep)
def create_workflow_step(step: WorkflowStepCreate):
    """Create a new workflow step"""
    new_id = max([s.id for s in workflow_steps_db]) + 1 if workflow_steps_db else 1
    new_step = WorkflowStep(
        id=new_id,
        **step.dict()
    )
    workflow_steps_db.append(new_step)
    return new_step

@router.put("/steps/{step_id}", response_model=WorkflowStep)
def update_workflow_step(step_id: int, step_update: WorkflowStepUpdate):
    """Update an existing workflow step"""
    for index, step in enumerate(workflow_steps_db):
        if step.id == step_id:
            updated_step = WorkflowStep(
                id=step_id,
                **step_update.dict()
            )
            workflow_steps_db[index] = updated_step
            return updated_step
    raise HTTPException(status_code=404, detail="Workflow step not found")

@router.delete("/steps/{step_id}")
def delete_workflow_step(step_id: int):
    """Delete a workflow step"""
    for index, step in enumerate(workflow_steps_db):
        if step.id == step_id:
            del workflow_steps_db[index]
            return {"message": "Workflow step deleted successfully"}
    raise HTTPException(status_code=404, detail="Workflow step not found")

@router.get("/workflows/{workflow_id}/steps", response_model=List[WorkflowStep])
def get_steps_for_workflow(workflow_id: int):
    """Get steps for a specific workflow"""
    return [step for step in workflow_steps_db if step.workflow_id == workflow_id]

# Scheduled Task endpoints
@router.get("/tasks", response_model=List[ScheduledTask])
def list_scheduled_tasks():
    """List all scheduled tasks"""
    return scheduled_tasks_db

@router.get("/tasks/{task_id}", response_model=ScheduledTask)
def get_scheduled_task(task_id: int):
    """Get a specific scheduled task by ID"""
    for task in scheduled_tasks_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Scheduled task not found")

@router.post("/tasks", response_model=ScheduledTask)
def create_scheduled_task(task: ScheduledTaskCreate):
    """Create a new scheduled task"""
    new_id = max([t.id for t in scheduled_tasks_db]) + 1 if scheduled_tasks_db else 1
    new_task = ScheduledTask(
        id=new_id,
        created_at=datetime.now(),
        **task.dict()
    )
    scheduled_tasks_db.append(new_task)
    return new_task

@router.put("/tasks/{task_id}", response_model=ScheduledTask)
def update_scheduled_task(task_id: int, task_update: ScheduledTaskUpdate):
    """Update an existing scheduled task"""
    for index, task in enumerate(scheduled_tasks_db):
        if task.id == task_id:
            updated_task = ScheduledTask(
                id=task_id,
                created_at=task.created_at,
                updated_at=datetime.now(),
                **task_update.dict()
            )
            scheduled_tasks_db[index] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Scheduled task not found")

@router.delete("/tasks/{task_id}")
def delete_scheduled_task(task_id: int):
    """Delete a scheduled task"""
    for index, task in enumerate(scheduled_tasks_db):
        if task.id == task_id:
            del scheduled_tasks_db[index]
            return {"message": "Scheduled task deleted successfully"}
    raise HTTPException(status_code=404, detail="Scheduled task not found")

@router.post("/tasks/{task_id}/activate")
def activate_scheduled_task(task_id: int):
    """Activate a scheduled task"""
    for index, task in enumerate(scheduled_tasks_db):
        if task.id == task_id:
            scheduled_tasks_db[index].is_active = True
            return {"message": "Scheduled task activated successfully"}
    raise HTTPException(status_code=404, detail="Scheduled task not found")

@router.post("/tasks/{task_id}/deactivate")
def deactivate_scheduled_task(task_id: int):
    """Deactivate a scheduled task"""
    for index, task in enumerate(scheduled_tasks_db):
        if task.id == task_id:
            scheduled_tasks_db[index].is_active = False
            return {"message": "Scheduled task deactivated successfully"}
    raise HTTPException(status_code=404, detail="Scheduled task not found")

@router.post("/tasks/{task_id}/run")
def run_scheduled_task(task_id: int):
    """Manually run a scheduled task"""
    for index, task in enumerate(scheduled_tasks_db):
        if task.id == task_id:
            scheduled_tasks_db[index].last_run_at = datetime.now()
            # In a real implementation, this would execute the task's action
            return {"message": "Scheduled task run successfully"}
    raise HTTPException(status_code=404, detail="Scheduled task not found")

# Configuration endpoints
@router.get("/config/automation-types", response_model=List[str])
def get_automation_type_options():
    """Get available automation type options"""
    return get_automation_types()

@router.get("/config/trigger-types", response_model=List[str])
def get_trigger_type_options():
    """Get available trigger type options"""
    return get_trigger_types()

@router.get("/config/action-types", response_model=List[str])
def get_action_type_options():
    """Get available action type options"""
    return get_action_types()