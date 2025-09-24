from fastapi import APIRouter, HTTPException, Depends
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from .models import (
    Workflow, WorkflowCreate, WorkflowUpdate,
    WorkflowStep, WorkflowStepCreate, WorkflowStepUpdate,
    LeadQualificationRule, LeadQualificationRuleCreate, LeadQualificationRuleUpdate,
    CustomerJourneyStage, CustomerJourneyStageCreate, CustomerJourneyStageUpdate,
    EventTrigger, EventTriggerCreate, EventTriggerUpdate
)
from .config import (
    get_workflow_statuses, get_trigger_types, get_action_types,
    get_default_execution_count, get_default_score_threshold
)

router = APIRouter(prefix="/automation", tags=["automation"])

# In-memory storage for demo purposes
workflows_db = []
workflow_steps_db = []
lead_qualification_rules_db = []
customer_journey_stages_db = []
event_triggers_db = []

@router.get("/")
def get_automation_dashboard():
    """Get marketing automation dashboard with summary statistics"""
    return {
        "message": "Marketing Automation Dashboard",
        "statistics": {
            "total_workflows": len(workflows_db),
            "active_workflows": len([w for w in workflows_db if w.status == "Active"]),
            "total_workflow_steps": len(workflow_steps_db),
            "total_qualification_rules": len(lead_qualification_rules_db),
            "total_journey_stages": len(customer_journey_stages_db),
            "total_event_triggers": len(event_triggers_db)
        }
    }

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
        execution_count=get_default_execution_count(),
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
                execution_count=workflow.execution_count,
                error_count=workflow.error_count,
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
            workflow.status = "Active"
            workflow.is_active = True
            workflows_db[index] = workflow
            return {"message": f"Workflow {workflow_id} activated successfully"}
    raise HTTPException(status_code=404, detail="Workflow not found")

@router.post("/workflows/{workflow_id}/pause")
def pause_workflow(workflow_id: int):
    """Pause a workflow"""
    for index, workflow in enumerate(workflows_db):
        if workflow.id == workflow_id:
            workflow.status = "Paused"
            workflow.is_active = False
            workflows_db[index] = workflow
            return {"message": f"Workflow {workflow_id} paused successfully"}
    raise HTTPException(status_code=404, detail="Workflow not found")

@router.get("/workflows/status/{status}", response_model=List[Workflow])
def get_workflows_by_status(status: str):
    """Get workflows by status"""
    # Normalize the status parameter to handle case differences
    normalized_status = status.lower().title()
    return [workflow for workflow in workflows_db if workflow.status == normalized_status]

# Workflow Steps endpoints
@router.get("/workflow-steps", response_model=List[WorkflowStep])
def list_workflow_steps():
    """List all workflow steps"""
    return workflow_steps_db

@router.get("/workflow-steps/{step_id}", response_model=WorkflowStep)
def get_workflow_step(step_id: int):
    """Get a specific workflow step by ID"""
    for step in workflow_steps_db:
        if step.id == step_id:
            return step
    raise HTTPException(status_code=404, detail="Workflow step not found")

@router.post("/workflow-steps", response_model=WorkflowStep)
def create_workflow_step(step: WorkflowStepCreate):
    """Create a new workflow step"""
    new_id = max([s.id for s in workflow_steps_db]) + 1 if workflow_steps_db else 1
    new_step = WorkflowStep(
        id=new_id,
        created_at=datetime.now(),
        **step.dict()
    )
    workflow_steps_db.append(new_step)
    return new_step

@router.put("/workflow-steps/{step_id}", response_model=WorkflowStep)
def update_workflow_step(step_id: int, step_update: WorkflowStepUpdate):
    """Update an existing workflow step"""
    for index, step in enumerate(workflow_steps_db):
        if step.id == step_id:
            updated_step = WorkflowStep(
                id=step_id,
                created_at=step.created_at,
                updated_at=datetime.now(),
                **step_update.dict()
            )
            workflow_steps_db[index] = updated_step
            return updated_step
    raise HTTPException(status_code=404, detail="Workflow step not found")

@router.delete("/workflow-steps/{step_id}")
def delete_workflow_step(step_id: int):
    """Delete a workflow step"""
    for index, step in enumerate(workflow_steps_db):
        if step.id == step_id:
            del workflow_steps_db[index]
            return {"message": "Workflow step deleted successfully"}
    raise HTTPException(status_code=404, detail="Workflow step not found")

@router.get("/workflow-steps/workflow/{workflow_id}", response_model=List[WorkflowStep])
def get_workflow_steps_by_workflow(workflow_id: int):
    """Get workflow steps by workflow ID"""
    return [step for step in workflow_steps_db if step.workflow_id == workflow_id]

# Lead Qualification Rules endpoints
@router.get("/qualification-rules", response_model=List[LeadQualificationRule])
def list_lead_qualification_rules():
    """List all lead qualification rules"""
    return lead_qualification_rules_db

@router.get("/qualification-rules/{rule_id}", response_model=LeadQualificationRule)
def get_lead_qualification_rule(rule_id: int):
    """Get a specific lead qualification rule by ID"""
    for rule in lead_qualification_rules_db:
        if rule.id == rule_id:
            return rule
    raise HTTPException(status_code=404, detail="Lead qualification rule not found")

@router.post("/qualification-rules", response_model=LeadQualificationRule)
def create_lead_qualification_rule(rule: LeadQualificationRuleCreate):
    """Create a new lead qualification rule"""
    new_id = max([r.id for r in lead_qualification_rules_db]) + 1 if lead_qualification_rules_db else 1
    new_rule = LeadQualificationRule(
        id=new_id,
        created_at=datetime.now(),
        qualified_lead_count=0,
        **rule.dict()
    )
    lead_qualification_rules_db.append(new_rule)
    return new_rule

@router.put("/qualification-rules/{rule_id}", response_model=LeadQualificationRule)
def update_lead_qualification_rule(rule_id: int, rule_update: LeadQualificationRuleUpdate):
    """Update an existing lead qualification rule"""
    for index, rule in enumerate(lead_qualification_rules_db):
        if rule.id == rule_id:
            updated_rule = LeadQualificationRule(
                id=rule_id,
                created_at=rule.created_at,
                updated_at=datetime.now(),
                qualified_lead_count=rule.qualified_lead_count,
                **rule_update.dict()
            )
            lead_qualification_rules_db[index] = updated_rule
            return updated_rule
    raise HTTPException(status_code=404, detail="Lead qualification rule not found")

@router.delete("/qualification-rules/{rule_id}")
def delete_lead_qualification_rule(rule_id: int):
    """Delete a lead qualification rule"""
    for index, rule in enumerate(lead_qualification_rules_db):
        if rule.id == rule_id:
            del lead_qualification_rules_db[index]
            return {"message": "Lead qualification rule deleted successfully"}
    raise HTTPException(status_code=404, detail="Lead qualification rule not found")

@router.post("/qualification-rules/{rule_id}/test")
def test_lead_qualification_rule(rule_id: int):
    """Test a lead qualification rule"""
    for rule in lead_qualification_rules_db:
        if rule.id == rule_id:
            # In a real implementation, you would test the rule against sample leads
            return {"message": f"Lead qualification rule {rule_id} tested successfully"}
    raise HTTPException(status_code=404, detail="Lead qualification rule not found")

# Customer Journey Stages endpoints
@router.get("/journey-stages", response_model=List[CustomerJourneyStage])
def list_customer_journey_stages():
    """List all customer journey stages"""
    return customer_journey_stages_db

@router.get("/journey-stages/{stage_id}", response_model=CustomerJourneyStage)
def get_customer_journey_stage(stage_id: int):
    """Get a specific customer journey stage by ID"""
    for stage in customer_journey_stages_db:
        if stage.id == stage_id:
            return stage
    raise HTTPException(status_code=404, detail="Customer journey stage not found")

@router.post("/journey-stages", response_model=CustomerJourneyStage)
def create_customer_journey_stage(stage: CustomerJourneyStageCreate):
    """Create a new customer journey stage"""
    new_id = max([s.id for s in customer_journey_stages_db]) + 1 if customer_journey_stages_db else 1
    new_stage = CustomerJourneyStage(
        id=new_id,
        created_at=datetime.now(),
        contact_count=0,
        **stage.dict()
    )
    customer_journey_stages_db.append(new_stage)
    return new_stage

@router.put("/journey-stages/{stage_id}", response_model=CustomerJourneyStage)
def update_customer_journey_stage(stage_id: int, stage_update: CustomerJourneyStageUpdate):
    """Update an existing customer journey stage"""
    for index, stage in enumerate(customer_journey_stages_db):
        if stage.id == stage_id:
            updated_stage = CustomerJourneyStage(
                id=stage_id,
                created_at=stage.created_at,
                updated_at=datetime.now(),
                contact_count=stage.contact_count,
                **stage_update.dict()
            )
            customer_journey_stages_db[index] = updated_stage
            return updated_stage
    raise HTTPException(status_code=404, detail="Customer journey stage not found")

@router.delete("/journey-stages/{stage_id}")
def delete_customer_journey_stage(stage_id: int):
    """Delete a customer journey stage"""
    for index, stage in enumerate(customer_journey_stages_db):
        if stage.id == stage_id:
            del customer_journey_stages_db[index]
            return {"message": "Customer journey stage deleted successfully"}
    raise HTTPException(status_code=404, detail="Customer journey stage not found")

# Event Triggers endpoints
@router.get("/event-triggers", response_model=List[EventTrigger])
def list_event_triggers():
    """List all event triggers"""
    return event_triggers_db

@router.get("/event-triggers/{trigger_id}", response_model=EventTrigger)
def get_event_trigger(trigger_id: int):
    """Get a specific event trigger by ID"""
    for trigger in event_triggers_db:
        if trigger.id == trigger_id:
            return trigger
    raise HTTPException(status_code=404, detail="Event trigger not found")

@router.post("/event-triggers", response_model=EventTrigger)
def create_event_trigger(trigger: EventTriggerCreate):
    """Create a new event trigger"""
    new_id = max([t.id for t in event_triggers_db]) + 1 if event_triggers_db else 1
    new_trigger = EventTrigger(
        id=new_id,
        created_at=datetime.now(),
        trigger_count=0,
        **trigger.dict()
    )
    event_triggers_db.append(new_trigger)
    return new_trigger

@router.put("/event-triggers/{trigger_id}", response_model=EventTrigger)
def update_event_trigger(trigger_id: int, trigger_update: EventTriggerUpdate):
    """Update an existing event trigger"""
    for index, trigger in enumerate(event_triggers_db):
        if trigger.id == trigger_id:
            updated_trigger = EventTrigger(
                id=trigger_id,
                created_at=trigger.created_at,
                updated_at=datetime.now(),
                trigger_count=trigger.trigger_count,
                **trigger_update.dict()
            )
            event_triggers_db[index] = updated_trigger
            return updated_trigger
    raise HTTPException(status_code=404, detail="Event trigger not found")

@router.delete("/event-triggers/{trigger_id}")
def delete_event_trigger(trigger_id: int):
    """Delete an event trigger"""
    for index, trigger in enumerate(event_triggers_db):
        if trigger.id == trigger_id:
            del event_triggers_db[index]
            return {"message": "Event trigger deleted successfully"}
    raise HTTPException(status_code=404, detail="Event trigger not found")

# Configuration endpoints
@router.get("/config/workflow-statuses", response_model=List[str])
def get_workflow_status_options():
    """Get available workflow statuses"""
    return get_workflow_statuses()

@router.get("/config/trigger-types", response_model=List[str])
def get_trigger_type_options():
    """Get available trigger types"""
    return get_trigger_types()

@router.get("/config/action-types", response_model=List[str])
def get_action_type_options():
    """Get available action types"""
    return get_action_types()