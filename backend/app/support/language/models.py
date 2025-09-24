from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
# Removed Enum import since we're removing static enums

# Removed LanguageCode enum
# Removed TranslationStatus enum

class SupportedLanguageBase(BaseModel):
    code: str  # Changed from LanguageCode to str
    name: str
    is_active: bool = True
    is_default: bool = False

class SupportedLanguageCreate(SupportedLanguageBase):
    pass

class SupportedLanguageUpdate(SupportedLanguageBase):
    pass

class SupportedLanguage(SupportedLanguageBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class UITranslationBase(BaseModel):
    language_id: int
    key: str
    original_text: str
    translated_text: str
    context: Optional[str] = None

class UITranslationCreate(UITranslationBase):
    pass

class UITranslationUpdate(UITranslationBase):
    pass

class UITranslation(UITranslationBase):
    id: int
    status: str = "Pending"  # Changed from TranslationStatus to str
    created_at: datetime
    updated_at: Optional[datetime] = None
    reviewed_at: Optional[datetime] = None
    reviewer_id: Optional[int] = None

class ContentTranslationBase(BaseModel):
    language_id: int
    content_type: str  # article, knowledge_base, email_template, etc.
    content_id: int
    title: Optional[str] = None
    content: str
    summary: Optional[str] = None

class ContentTranslationCreate(ContentTranslationBase):
    pass

class ContentTranslationUpdate(ContentTranslationBase):
    pass

class ContentTranslation(ContentTranslationBase):
    id: int
    status: str = "Pending"  # Changed from TranslationStatus to str
    created_at: datetime
    updated_at: Optional[datetime] = None
    translated_by: Optional[int] = None
    reviewed_at: Optional[datetime] = None
    reviewer_id: Optional[int] = None

class TranslationMemoryBase(BaseModel):
    source_text: str
    target_text: str
    source_language_id: int
    target_language_id: int
    context: Optional[str] = None
    is_approved: bool = True

class TranslationMemoryCreate(TranslationMemoryBase):
    pass

class TranslationMemoryUpdate(TranslationMemoryBase):
    pass

class TranslationMemory(TranslationMemoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class LanguageDetectionBase(BaseModel):
    text: str
    detected_language: str  # Changed from LanguageCode to str
    confidence: float  # 0.0 to 1.0

class LanguageDetectionCreate(LanguageDetectionBase):
    pass

class LanguageDetection(LanguageDetectionBase):
    id: int
    created_at: datetime