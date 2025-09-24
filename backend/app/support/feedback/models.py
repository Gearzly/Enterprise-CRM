from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
# Removed Enum import since we're removing static enums

# Removed FeedbackType enum
# Removed FeedbackStatus enum
# Removed FeedbackCategory enum

class FeedbackBase(BaseModel):
    customer_id: int
    type: str  # Changed from FeedbackType to str
    subject: str
    description: str
    category: str = "Other"  # Changed from FeedbackCategory to str
    status: str = "Pending"  # Changed from FeedbackStatus to str
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