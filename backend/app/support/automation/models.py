from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class AutomationType(str, Enum):
    ticket_routing = "Ticket Routing"
    auto_response = "Auto Response"
    escalation = "Escalation"
    follow_up = "Follow Up"
    notification = "Notification"

class AutomationStatus(str, Enum):
    active = "Active"
    inactive = "Inactive"
    paused = "Paused"

class TriggerType(str, Enum):
    ticket_created = "Ticket Created"
    ticket_updated = "Ticket Updated"
    ticket_status_changed = "Ticket Status Changed"
    ticket_priority_changed = "Ticket Priority Changed"
    time_based = "Time Based"

class ActionType(str, Enum):
    assign_ticket = "Assign Ticket"
    send_email = "Send Email"
    send_notification = "Send Notification"
    update_ticket = "Update Ticket"
    create_task = "Create Task"

class AutomationRuleBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: AutomationType
    trigger_type: TriggerType
    conditions: Dict[str, Any] = {}
    actions: List[Dict[str, Any]] = []
    is_active: bool = True
    priority: int = 1

class AutomationRuleCreate(AutomationRuleBase):
    pass

class AutomationRuleUpdate(AutomationRuleBase):
    pass

class AutomationRule(AutomationRuleBase):
    id: int
    status: AutomationStatus = AutomationStatus.active
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_triggered_at: Optional[datetime] = None
    trigger_count: int = 0

class WorkflowBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True

class WorkflowCreate(WorkflowBase):
    pass

class WorkflowUpdate(WorkflowBase):
    pass

class Workflow(WorkflowBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class WorkflowStepBase(BaseModel):
    workflow_id: int
    name: str
    description: Optional[str] = None
    order: int
    conditions: Dict[str, Any] = {}
    actions: List[Dict[str, Any]] = []
    next_step_id: Optional[int] = None

class WorkflowStepCreate(WorkflowStepBase):
    pass

class WorkflowStepUpdate(WorkflowStepBase):
    pass

class WorkflowStep(WorkflowStepBase):
    id: int

class ScheduledTaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    cron_expression: str
    action: Dict[str, Any]
    is_active: bool = True

class ScheduledTaskCreate(ScheduledTaskBase):
    pass

class ScheduledTaskUpdate(ScheduledTaskBase):
    pass

class ScheduledTask(ScheduledTaskBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_run_at: Optional[datetime] = None
    next_run_at: Optional[datetime] = None