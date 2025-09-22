from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class WorkflowStatus(str, Enum):
    draft = "Draft"
    active = "Active"
    paused = "Paused"
    completed = "Completed"
    error = "Error"

class TriggerType(str, Enum):
    form_submission = "Form Submission"
    email_open = "Email Open"
    email_click = "Email Click"
    website_visit = "Website Visit"
    download = "Download"
    purchase = "Purchase"
    webinar_attendance = "Webinar Attendance"
    custom_event = "Custom Event"

class ActionType(str, Enum):
    send_email = "Send Email"
    update_contact = "Update Contact"
    add_tag = "Add Tag"
    remove_tag = "Remove Tag"
    assign_owner = "Assign Owner"
    send_notification = "Send Notification"
    add_to_list = "Add to List"
    remove_from_list = "Remove from List"
    score_lead = "Score Lead"
    create_task = "Create Task"
    custom_action = "Custom Action"

class WorkflowBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: WorkflowStatus = WorkflowStatus.draft
    trigger_type: TriggerType
    trigger_criteria: Dict[str, Any]  # JSON structure for trigger criteria
    is_active: bool = True

class WorkflowCreate(WorkflowBase):
    pass

class WorkflowUpdate(WorkflowBase):
    pass

class Workflow(WorkflowBase):
    id: int
    execution_count: int = 0
    error_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

class WorkflowStepBase(BaseModel):
    workflow_id: int
    action_type: ActionType
    action_config: Dict[str, Any]  # JSON structure for action configuration
    step_order: int
    delay_minutes: int = 0
    condition: Optional[str] = None  # Condition to execute this step

class WorkflowStepCreate(WorkflowStepBase):
    pass

class WorkflowStepUpdate(WorkflowStepBase):
    pass

class WorkflowStep(WorkflowStepBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class LeadQualificationRuleBase(BaseModel):
    name: str
    description: Optional[str] = None
    criteria: Dict[str, Any]  # JSON structure for qualification criteria
    score_threshold: int
    is_active: bool = True

class LeadQualificationRuleCreate(LeadQualificationRuleBase):
    pass

class LeadQualificationRuleUpdate(LeadQualificationRuleBase):
    pass

class LeadQualificationRule(LeadQualificationRuleBase):
    id: int
    qualified_lead_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

class CustomerJourneyStageBase(BaseModel):
    name: str
    description: Optional[str] = None
    order: int
    criteria: Dict[str, Any]  # JSON structure for stage criteria

class CustomerJourneyStageCreate(CustomerJourneyStageBase):
    pass

class CustomerJourneyStageUpdate(CustomerJourneyStageBase):
    pass

class CustomerJourneyStage(CustomerJourneyStageBase):
    id: int
    contact_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

class EventTriggerBase(BaseModel):
    name: str
    description: Optional[str] = None
    event_type: str  # e.g., "birthday", "anniversary", "contract_renewal"
    trigger_date_field: str  # Field to calculate trigger date from
    days_before: int = 0
    days_after: int = 0
    is_active: bool = True

class EventTriggerCreate(EventTriggerBase):
    pass

class EventTriggerUpdate(EventTriggerBase):
    pass

class EventTrigger(EventTriggerBase):
    id: int
    trigger_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None