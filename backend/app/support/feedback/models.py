from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class FeedbackType(str, Enum):
    survey = "Survey"
    nps = "NPS"
    general = "General"
    feature_request = "Feature Request"
    bug_report = "Bug Report"

class FeedbackStatus(str, Enum):
    pending = "Pending"
    reviewed = "Reviewed"
    addressed = "Addressed"
    archived = "Archived"

class FeedbackCategory(str, Enum):
    product = "Product"
    service = "Service"
    support = "Support"
    billing = "Billing"
    other = "Other"

class FeedbackBase(BaseModel):
    customer_id: int
    type: FeedbackType
    subject: str
    description: str
    category: FeedbackCategory = FeedbackCategory.other
    status: FeedbackStatus = FeedbackStatus.pending
    priority: int = 1  # 1-5 scale
    tags: List[str] = []

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackUpdate(FeedbackBase):
    pass

class Feedback(FeedbackBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class SurveyBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True

class SurveyCreate(SurveyBase):
    pass

class SurveyUpdate(SurveyBase):
    pass

class Survey(SurveyBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class SurveyQuestionBase(BaseModel):
    survey_id: int
    question_text: str
    question_type: str  # text, rating, multiple_choice, etc.
    is_required: bool = True
    order: int

class SurveyQuestionCreate(SurveyQuestionBase):
    pass

class SurveyQuestionUpdate(SurveyQuestionBase):
    pass

class SurveyQuestion(SurveyQuestionBase):
    id: int

class SurveyResponseBase(BaseModel):
    survey_id: int
    customer_id: int
    question_id: int
    response: str

class SurveyResponseCreate(SurveyResponseBase):
    pass

class SurveyResponse(SurveyResponseBase):
    id: int
    created_at: datetime