from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from .models import (
    SupportedLanguage, SupportedLanguageCreate, SupportedLanguageUpdate,
    UITranslation, UITranslationCreate, UITranslationUpdate,
    ContentTranslation, ContentTranslationCreate, ContentTranslationUpdate,
    TranslationMemory, TranslationMemoryCreate, TranslationMemoryUpdate,
    LanguageDetection, LanguageDetectionCreate
)
from .config import (
    get_supported_languages, get_default_language, get_translation_statuses,
    get_max_confidence_threshold, get_min_confidence_threshold
)

router = APIRouter()

# In-memory storage for demo purposes
supported_languages_db = []
ui_translations_db = []
content_translations_db = []
translation_memories_db = []
language_detections_db = []

@router.get("/languages", response_model=List[SupportedLanguage])
def list_supported_languages():
    """List all supported languages"""
    return supported_languages_db

@router.get("/languages/{language_id}", response_model=SupportedLanguage)
def get_supported_language(language_id: int):
    """Get a specific supported language by ID"""
    for language in supported_languages_db:
        if language.id == language_id:
            return language
    raise HTTPException(status_code=404, detail="Supported language not found")

@router.post("/languages", response_model=SupportedLanguage)
def create_supported_language(language: SupportedLanguageCreate):
    """Create a new supported language"""
    new_id = max([l.id for l in supported_languages_db]) + 1 if supported_languages_db else 1
    new_language = SupportedLanguage(
        id=new_id,
        created_at=datetime.now(),
        **language.dict()
    )
    supported_languages_db.append(new_language)
    return new_language

@router.put("/languages/{language_id}", response_model=SupportedLanguage)
def update_supported_language(language_id: int, language_update: SupportedLanguageUpdate):
    """Update an existing supported language"""
    for index, language in enumerate(supported_languages_db):
        if language.id == language_id:
            updated_language = SupportedLanguage(
                id=language_id,
                created_at=language.created_at,
                updated_at=datetime.now(),
                **language_update.dict()
            )
            supported_languages_db[index] = updated_language
            return updated_language
    raise HTTPException(status_code=404, detail="Supported language not found")

@router.delete("/languages/{language_id}")
def delete_supported_language(language_id: int):
    """Delete a supported language"""
    for index, language in enumerate(supported_languages_db):
        if language.id == language_id:
            del supported_languages_db[index]
            return {"message": "Supported language deleted successfully"}
    raise HTTPException(status_code=404, detail="Supported language not found")

@router.post("/languages/{language_id}/activate")
def activate_supported_language(language_id: int):
    """Activate a supported language"""
    for index, language in enumerate(supported_languages_db):
        if language.id == language_id:
            supported_languages_db[index].is_active = True
            return {"message": "Supported language activated successfully"}
    raise HTTPException(status_code=404, detail="Supported language not found")

@router.post("/languages/{language_id}/deactivate")
def deactivate_supported_language(language_id: int):
    """Deactivate a supported language"""
    for index, language in enumerate(supported_languages_db):
        if language.id == language_id:
            supported_languages_db[index].is_active = False
            return {"message": "Supported language deactivated successfully"}
    raise HTTPException(status_code=404, detail="Supported language not found")

@router.post("/languages/{language_id}/set-default")
def set_default_language(language_id: int):
    """Set a language as the default language"""
    # First, unset the current default language
    for index, language in enumerate(supported_languages_db):
        if language.is_default:
            supported_languages_db[index].is_default = False
    
    # Then set the new default language
    for index, language in enumerate(supported_languages_db):
        if language.id == language_id:
            supported_languages_db[index].is_default = True
            return {"message": "Default language set successfully"}
    raise HTTPException(status_code=404, detail="Supported language not found")

@router.get("/languages/default", response_model=SupportedLanguage)
def get_default_supported_language():
    """Get the default supported language"""
    for language in supported_languages_db:
        if language.is_default:
            return language
    raise HTTPException(status_code=404, detail="Default language not found")

# UI Translation endpoints
@router.get("/ui", response_model=List[UITranslation])
def list_ui_translations():
    """List all UI translations"""
    return ui_translations_db

@router.get("/ui/{translation_id}", response_model=UITranslation)
def get_ui_translation(translation_id: int):
    """Get a specific UI translation by ID"""
    for translation in ui_translations_db:
        if translation.id == translation_id:
            return translation
    raise HTTPException(status_code=404, detail="UI translation not found")

@router.post("/ui", response_model=UITranslation)
def create_ui_translation(translation: UITranslationCreate):
    """Create a new UI translation"""
    new_id = max([t.id for t in ui_translations_db]) + 1 if ui_translations_db else 1
    new_translation = UITranslation(
        id=new_id,
        created_at=datetime.now(),
        **translation.dict()
    )
    ui_translations_db.append(new_translation)
    return new_translation

@router.put("/ui/{translation_id}", response_model=UITranslation)
def update_ui_translation(translation_id: int, translation_update: UITranslationUpdate):
    """Update an existing UI translation"""
    for index, translation in enumerate(ui_translations_db):
        if translation.id == translation_id:
            updated_translation = UITranslation(
                id=translation_id,
                created_at=translation.created_at,
                updated_at=datetime.now(),
                **translation_update.dict()
            )
            ui_translations_db[index] = updated_translation
            return updated_translation
    raise HTTPException(status_code=404, detail="UI translation not found")

@router.delete("/ui/{translation_id}")
def delete_ui_translation(translation_id: int):
    """Delete a UI translation"""
    for index, translation in enumerate(ui_translations_db):
        if translation.id == translation_id:
            del ui_translations_db[index]
            return {"message": "UI translation deleted successfully"}
    raise HTTPException(status_code=404, detail="UI translation not found")

@router.post("/ui/{translation_id}/review")
def review_ui_translation(translation_id: int, reviewer_id: int):
    """Mark a UI translation as reviewed"""
    for index, translation in enumerate(ui_translations_db):
        if translation.id == translation_id:
            ui_translations_db[index].status = "Reviewed"
            ui_translations_db[index].reviewed_at = datetime.now()
            ui_translations_db[index].reviewer_id = reviewer_id
            return {"message": "UI translation reviewed successfully"}
    raise HTTPException(status_code=404, detail="UI translation not found")

@router.post("/ui/{translation_id}/publish")
def publish_ui_translation(translation_id: int):
    """Publish a UI translation"""
    for index, translation in enumerate(ui_translations_db):
        if translation.id == translation_id:
            ui_translations_db[index].status = "Published"
            return {"message": "UI translation published successfully"}
    raise HTTPException(status_code=404, detail="UI translation not found")

@router.get("/ui/language/{language_id}", response_model=List[UITranslation])
def get_ui_translations_by_language(language_id: int):
    """Get UI translations by language"""
    return [translation for translation in ui_translations_db if translation.language_id == language_id]

@router.get("/ui/key/{key}", response_model=List[UITranslation])
def get_ui_translations_by_key(key: str):
    """Get UI translations by key"""
    return [translation for translation in ui_translations_db if translation.key == key]

@router.get("/ui/status/{status}", response_model=List[UITranslation])
def get_ui_translations_by_status(status: str):
    """Get UI translations by status"""
    # Normalize the status parameter to handle case differences
    normalized_status = status.lower().title()
    return [translation for translation in ui_translations_db if translation.status.value == normalized_status]

# Content Translation endpoints
@router.get("/content", response_model=List[ContentTranslation])
def list_content_translations():
    """List all content translations"""
    return content_translations_db

@router.get("/content/{translation_id}", response_model=ContentTranslation)
def get_content_translation(translation_id: int):
    """Get a specific content translation by ID"""
    for translation in content_translations_db:
        if translation.id == translation_id:
            return translation
    raise HTTPException(status_code=404, detail="Content translation not found")

@router.post("/content", response_model=ContentTranslation)
def create_content_translation(translation: ContentTranslationCreate):
    """Create a new content translation"""
    new_id = max([t.id for t in content_translations_db]) + 1 if content_translations_db else 1
    new_translation = ContentTranslation(
        id=new_id,
        created_at=datetime.now(),
        **translation.dict()
    )
    content_translations_db.append(new_translation)
    return new_translation

@router.put("/content/{translation_id}", response_model=ContentTranslation)
def update_content_translation(translation_id: int, translation_update: ContentTranslationUpdate):
    """Update an existing content translation"""
    for index, translation in enumerate(content_translations_db):
        if translation.id == translation_id:
            updated_translation = ContentTranslation(
                id=translation_id,
                created_at=translation.created_at,
                updated_at=datetime.now(),
                **translation_update.dict()
            )
            content_translations_db[index] = updated_translation
            return updated_translation
    raise HTTPException(status_code=404, detail="Content translation not found")

@router.delete("/content/{translation_id}")
def delete_content_translation(translation_id: int):
    """Delete a content translation"""
    for index, translation in enumerate(content_translations_db):
        if translation.id == translation_id:
            del content_translations_db[index]
            return {"message": "Content translation deleted successfully"}
    raise HTTPException(status_code=404, detail="Content translation not found")

@router.post("/content/{translation_id}/review")
def review_content_translation(translation_id: int, reviewer_id: int):
    """Mark a content translation as reviewed"""
    for index, translation in enumerate(content_translations_db):
        if translation.id == translation_id:
            content_translations_db[index].status = "Reviewed"
            content_translations_db[index].reviewed_at = datetime.now()
            content_translations_db[index].reviewer_id = reviewer_id
            return {"message": "Content translation reviewed successfully"}
    raise HTTPException(status_code=404, detail="Content translation not found")

@router.post("/content/{translation_id}/publish")
def publish_content_translation(translation_id: int):
    """Publish a content translation"""
    for index, translation in enumerate(content_translations_db):
        if translation.id == translation_id:
            content_translations_db[index].status = "Published"
            return {"message": "Content translation published successfully"}
    raise HTTPException(status_code=404, detail="Content translation not found")

@router.get("/content/language/{language_id}", response_model=List[ContentTranslation])
def get_content_translations_by_language(language_id: int):
    """Get content translations by language"""
    return [translation for translation in content_translations_db if translation.language_id == language_id]

@router.get("/content/type/{content_type}", response_model=List[ContentTranslation])
def get_content_translations_by_type(content_type: str):
    """Get content translations by content type"""
    return [translation for translation in content_translations_db if translation.content_type == content_type]

@router.get("/content/type/{content_type}/id/{content_id}", response_model=List[ContentTranslation])
def get_content_translations_by_content(content_type: str, content_id: int):
    """Get content translations by content type and ID"""
    return [translation for translation in content_translations_db 
            if translation.content_type == content_type and translation.content_id == content_id]

# Translation Memory endpoints
@router.get("/memory", response_model=List[TranslationMemory])
def list_translation_memories():
    """List all translation memories"""
    return translation_memories_db

@router.get("/memory/{memory_id}", response_model=TranslationMemory)
def get_translation_memory(memory_id: int):
    """Get a specific translation memory by ID"""
    for memory in translation_memories_db:
        if memory.id == memory_id:
            return memory
    raise HTTPException(status_code=404, detail="Translation memory not found")

@router.post("/memory", response_model=TranslationMemory)
def create_translation_memory(memory: TranslationMemoryCreate):
    """Create a new translation memory"""
    new_id = max([m.id for m in translation_memories_db]) + 1 if translation_memories_db else 1
    new_memory = TranslationMemory(
        id=new_id,
        created_at=datetime.now(),
        **memory.dict()
    )
    translation_memories_db.append(new_memory)
    return new_memory

@router.put("/memory/{memory_id}", response_model=TranslationMemory)
def update_translation_memory(memory_id: int, memory_update: TranslationMemoryUpdate):
    """Update an existing translation memory"""
    for index, memory in enumerate(translation_memories_db):
        if memory.id == memory_id:
            updated_memory = TranslationMemory(
                id=memory_id,
                created_at=memory.created_at,
                updated_at=datetime.now(),
                **memory_update.dict()
            )
            translation_memories_db[index] = updated_memory
            return updated_memory
    raise HTTPException(status_code=404, detail="Translation memory not found")

@router.delete("/memory/{memory_id}")
def delete_translation_memory(memory_id: int):
    """Delete a translation memory"""
    for index, memory in enumerate(translation_memories_db):
        if memory.id == memory_id:
            del translation_memories_db[index]
            return {"message": "Translation memory deleted successfully"}
    raise HTTPException(status_code=404, detail="Translation memory not found")

@router.post("/memory/{memory_id}/approve")
def approve_translation_memory(memory_id: int):
    """Approve a translation memory"""
    for index, memory in enumerate(translation_memories_db):
        if memory.id == memory_id:
            translation_memories_db[index].is_approved = True
            return {"message": "Translation memory approved successfully"}
    raise HTTPException(status_code=404, detail="Translation memory not found")

@router.post("/memory/{memory_id}/reject")
def reject_translation_memory(memory_id: int):
    """Reject a translation memory"""
    for index, memory in enumerate(translation_memories_db):
        if memory.id == memory_id:
            translation_memories_db[index].is_approved = False
            return {"message": "Translation memory rejected successfully"}
    raise HTTPException(status_code=404, detail="Translation memory not found")

@router.get("/memory/search", response_model=List[TranslationMemory])
def search_translation_memories(source_text: str, source_language_id: int, target_language_id: int):
    """Search translation memories"""
    results = []
    for memory in translation_memories_db:
        if (memory.source_text.lower() == source_text.lower() and
            memory.source_language_id == source_language_id and
            memory.target_language_id == target_language_id):
            results.append(memory)
    return results

# Language Detection endpoints
@router.get("/detections", response_model=List[LanguageDetection])
def list_language_detections():
    """List all language detections"""
    return language_detections_db

@router.get("/detections/{detection_id}", response_model=LanguageDetection)
def get_language_detection(detection_id: int):
    """Get a specific language detection by ID"""
    for detection in language_detections_db:
        if detection.id == detection_id:
            return detection
    raise HTTPException(status_code=404, detail="Language detection not found")

@router.post("/detections", response_model=LanguageDetection)
def create_language_detection(detection: LanguageDetectionCreate):
    """Create a new language detection"""
    new_id = max([d.id for d in language_detections_db]) + 1 if language_detections_db else 1
    new_detection = LanguageDetection(
        id=new_id,
        created_at=datetime.now(),
        **detection.dict()
    )
    language_detections_db.append(new_detection)
    return new_detection

@router.get("/detections/confident", response_model=List[LanguageDetection])
def get_confident_language_detections():
    """Get language detections with high confidence"""
    max_threshold = get_max_confidence_threshold()
    return [detection for detection in language_detections_db if detection.confidence >= max_threshold]

@router.get("/detections/uncertain", response_model=List[LanguageDetection])
def get_uncertain_language_detections():
    """Get language detections with low confidence"""
    min_threshold = get_min_confidence_threshold()
    return [detection for detection in language_detections_db if detection.confidence < min_threshold]

# Configuration endpoints
@router.get("/config/languages", response_model=List[str])
def get_supported_language_options():
    """Get supported language options"""
    return get_supported_languages()

@router.get("/config/default-language", response_model=str)
def get_default_language_code():
    """Get default language code"""
    return get_default_language()

@router.get("/config/statuses", response_model=List[str])
def get_translation_status_options():
    """Get available translation status options"""
    return get_translation_statuses()

@router.get("/config/max-confidence", response_model=float)
def get_max_confidence_threshold_value():
    """Get maximum confidence threshold"""
    return get_max_confidence_threshold()

@router.get("/config/min-confidence", response_model=float)
def get_min_confidence_threshold_value():
    """Get minimum confidence threshold"""
    return get_min_confidence_threshold()