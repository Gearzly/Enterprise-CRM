from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
# Removed Enum import since we're removing static enums

# Removed AutomationType enum
# Removed AutomationStatus enum
# Removed TriggerType enum
# Removed ActionType enum

class AutomationRuleBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: str  # Changed from AutomationType to str
    trigger_type: str  # Changed from TriggerType to str
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
    status: str = "Active"  # Changed from AutomationStatus to str
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