from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .models import (
    Feedback, FeedbackCreate, FeedbackUpdate,
    Survey, SurveyCreate, SurveyUpdate,
    SurveyQuestion, SurveyQuestionCreate, SurveyQuestionUpdate,
    SurveyResponse, SurveyResponseCreate
)
from .config import (
    get_feedback_types, get_feedback_categories, get_feedback_statuses,
    get_default_category, get_default_status, get_max_tags_per_feedback
)

router = APIRouter(prefix="/feedback", tags=["feedback"])

# In-memory storage for demo purposes
feedback_db = []
surveys_db = []
survey_questions_db = []
survey_responses_db = []

@router.get("/")
def get_feedback_dashboard():
    """Get support feedback dashboard with summary statistics"""
    return {
        "message": "Support Feedback Dashboard",
        "statistics": {
            "total_feedback": len(feedback_db),
            "total_surveys": len(surveys_db),
            "total_questions": len(survey_questions_db),
            "total_responses": len(survey_responses_db)
        }
    }

@router.get("/feedback", response_model=List[Feedback])
def list_feedback():
    """List all feedback"""
    return feedback_db

@router.get("/{feedback_id}", response_model=Feedback)
def get_feedback(feedback_id: int):
    """Get a specific feedback by ID"""
    for feedback in feedback_db:
        if feedback.id == feedback_id:
            return feedback
    raise HTTPException(status_code=404, detail="Feedback not found")

@router.post("/", response_model=Feedback)
def create_feedback(feedback: FeedbackCreate):
    """Create a new feedback"""
    new_id = max([f.id for f in feedback_db]) + 1 if feedback_db else 1
    new_feedback = Feedback(
        id=new_id,
        created_at=datetime.now(),
        **feedback.dict()
    )
    feedback_db.append(new_feedback)
    return new_feedback

@router.put("/{feedback_id}", response_model=Feedback)
def update_feedback(feedback_id: int, feedback_update: FeedbackUpdate):
    """Update an existing feedback"""
    for index, feedback in enumerate(feedback_db):
        if feedback.id == feedback_id:
            updated_feedback = Feedback(
                id=feedback_id,
                created_at=feedback.created_at,
                updated_at=datetime.now(),
                **feedback_update.dict()
            )
            feedback_db[index] = updated_feedback
            return updated_feedback
    raise HTTPException(status_code=404, detail="Feedback not found")

@router.delete("/{feedback_id}")
def delete_feedback(feedback_id: int):
    """Delete a feedback"""
    for index, feedback in enumerate(feedback_db):
        if feedback.id == feedback_id:
            del feedback_db[index]
            return {"message": "Feedback deleted successfully"}
    raise HTTPException(status_code=404, detail="Feedback not found")

@router.post("/{feedback_id}/review")
def review_feedback(feedback_id: int):
    """Mark feedback as reviewed"""
    for index, feedback in enumerate(feedback_db):
        if feedback.id == feedback_id:
            feedback_db[index].status = "Reviewed"
            return {"message": "Feedback marked as reviewed"}
    raise HTTPException(status_code=404, detail="Feedback not found")

@router.post("/{feedback_id}/address")
def address_feedback(feedback_id: int):
    """Mark feedback as addressed"""
    for index, feedback in enumerate(feedback_db):
        if feedback.id == feedback_id:
            feedback_db[index].status = "Addressed"
            return {"message": "Feedback marked as addressed"}
    raise HTTPException(status_code=404, detail="Feedback not found")

@router.get("/customer/{customer_id}", response_model=List[Feedback])
def get_feedback_by_customer(customer_id: int):
    """Get feedback by customer ID"""
    return [feedback for feedback in feedback_db if feedback.customer_id == customer_id]

@router.get("/type/{type}", response_model=List[Feedback])
def get_feedback_by_type(type: str):
    """Get feedback by type"""
    # Normalize the type parameter to handle case differences
    normalized_type = type.lower().title()
    return [feedback for feedback in feedback_db if feedback.type == normalized_type]

@router.get("/category/{category}", response_model=List[Feedback])
def get_feedback_by_category(category: str):
    """Get feedback by category"""
    # Normalize the category parameter to handle case differences
    normalized_category = category.lower().title()
    return [feedback for feedback in feedback_db if feedback.category == normalized_category]

@router.get("/status/{status}", response_model=List[Feedback])
def get_feedback_by_status(status: str):
    """Get feedback by status"""
    # Normalize the status parameter to handle case differences
    normalized_status = status.lower().title()
    return [feedback for feedback in feedback_db if feedback.status == normalized_status]

# Survey endpoints
@router.get("/surveys", response_model=List[Survey])
def list_surveys():
    """List all surveys"""
    return surveys_db

@router.get("/surveys/{survey_id}", response_model=Survey)
def get_survey(survey_id: int):
    """Get a specific survey by ID"""
    for survey in surveys_db:
        if survey.id == survey_id:
            return survey
    raise HTTPException(status_code=404, detail="Survey not found")

@router.post("/surveys", response_model=Survey)
def create_survey(survey: SurveyCreate):
    """Create a new survey"""
    new_id = max([s.id for s in surveys_db]) + 1 if surveys_db else 1
    new_survey = Survey(
        id=new_id,
        created_at=datetime.now(),
        **survey.dict()
    )
    surveys_db.append(new_survey)
    return new_survey

@router.put("/surveys/{survey_id}", response_model=Survey)
def update_survey(survey_id: int, survey_update: SurveyUpdate):
    """Update an existing survey"""
    for index, survey in enumerate(surveys_db):
        if survey.id == survey_id:
            updated_survey = Survey(
                id=survey_id,
                created_at=survey.created_at,
                updated_at=datetime.now(),
                **survey_update.dict()
            )
            surveys_db[index] = updated_survey
            return updated_survey
    raise HTTPException(status_code=404, detail="Survey not found")

@router.delete("/surveys/{survey_id}")
def delete_survey(survey_id: int):
    """Delete a survey"""
    for index, survey in enumerate(surveys_db):
        if survey.id == survey_id:
            del surveys_db[index]
            return {"message": "Survey deleted successfully"}
    raise HTTPException(status_code=404, detail="Survey not found")

@router.post("/surveys/{survey_id}/activate")
def activate_survey(survey_id: int):
    """Activate a survey"""
    for index, survey in enumerate(surveys_db):
        if survey.id == survey_id:
            surveys_db[index].is_active = True
            return {"message": "Survey activated successfully"}
    raise HTTPException(status_code=404, detail="Survey not found")

@router.post("/surveys/{survey_id}/deactivate")
def deactivate_survey(survey_id: int):
    """Deactivate a survey"""
    for index, survey in enumerate(surveys_db):
        if survey.id == survey_id:
            surveys_db[index].is_active = False
            return {"message": "Survey deactivated successfully"}
    raise HTTPException(status_code=404, detail="Survey not found")

# Survey Question endpoints
@router.get("/questions", response_model=List[SurveyQuestion])
def list_survey_questions():
    """List all survey questions"""
    return survey_questions_db

@router.get("/questions/{question_id}", response_model=SurveyQuestion)
def get_survey_question(question_id: int):
    """Get a specific survey question by ID"""
    for question in survey_questions_db:
        if question.id == question_id:
            return question
    raise HTTPException(status_code=404, detail="Survey question not found")

@router.post("/questions", response_model=SurveyQuestion)
def create_survey_question(question: SurveyQuestionCreate):
    """Create a new survey question"""
    new_id = max([q.id for q in survey_questions_db]) + 1 if survey_questions_db else 1
    new_question = SurveyQuestion(
        id=new_id,
        **question.dict()
    )
    survey_questions_db.append(new_question)
    return new_question

@router.put("/questions/{question_id}", response_model=SurveyQuestion)
def update_survey_question(question_id: int, question_update: SurveyQuestionUpdate):
    """Update an existing survey question"""
    for index, question in enumerate(survey_questions_db):
        if question.id == question_id:
            updated_question = SurveyQuestion(
                id=question_id,
                **question_update.dict()
            )
            survey_questions_db[index] = updated_question
            return updated_question
    raise HTTPException(status_code=404, detail="Survey question not found")

@router.delete("/questions/{question_id}")
def delete_survey_question(question_id: int):
    """Delete a survey question"""
    for index, question in enumerate(survey_questions_db):
        if question.id == question_id:
            del survey_questions_db[index]
            return {"message": "Survey question deleted successfully"}
    raise HTTPException(status_code=404, detail="Survey question not found")

@router.get("/surveys/{survey_id}/questions", response_model=List[SurveyQuestion])
def get_questions_for_survey(survey_id: int):
    """Get questions for a specific survey"""
    return [question for question in survey_questions_db if question.survey_id == survey_id]

# Survey Response endpoints
@router.get("/responses", response_model=List[SurveyResponse])
def list_survey_responses():
    """List all survey responses"""
    return survey_responses_db

@router.get("/responses/{response_id}", response_model=SurveyResponse)
def get_survey_response(response_id: int):
    """Get a specific survey response by ID"""
    for response in survey_responses_db:
        if response.id == response_id:
            return response
    raise HTTPException(status_code=404, detail="Survey response not found")

@router.post("/responses", response_model=SurveyResponse)
def create_survey_response(response: SurveyResponseCreate):
    """Create a new survey response"""
    new_id = max([r.id for r in survey_responses_db]) + 1 if survey_responses_db else 1
    new_response = SurveyResponse(
        id=new_id,
        created_at=datetime.now(),
        **response.dict()
    )
    survey_responses_db.append(new_response)
    return new_response

@router.get("/surveys/{survey_id}/responses", response_model=List[SurveyResponse])
def get_responses_for_survey(survey_id: int):
    """Get responses for a specific survey"""
    return [response for response in survey_responses_db if response.survey_id == survey_id]

@router.get("/customers/{customer_id}/responses", response_model=List[SurveyResponse])
def get_responses_for_customer(customer_id: int):
    """Get responses for a specific customer"""
    return [response for response in survey_responses_db if response.customer_id == customer_id]

# Configuration endpoints
@router.get("/config/types", response_model=List[str])
def get_feedback_type_options():
    """Get available feedback type options"""
    return get_feedback_types()

@router.get("/config/categories", response_model=List[str])
def get_feedback_category_options():
    """Get available feedback category options"""
    return get_feedback_categories()

@router.get("/config/statuses", response_model=List[str])
def get_feedback_status_options():
    """Get available feedback status options"""
    return get_feedback_statuses()