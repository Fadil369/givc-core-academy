"""
Translation models for TTLINC
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from uuid import UUID, uuid4

from pydantic import Field

from .base import BaseModel, TimestampMixin, LanguageCode


class DocumentType(str, Enum):
    """Medical document types"""
    CLINICAL_NOTE = "clinical_note"
    DISCHARGE_SUMMARY = "discharge_summary"
    LAB_REPORT = "lab_report"
    RADIOLOGY_REPORT = "radiology_report"
    PRESCRIPTION = "prescription"
    CONSENT_FORM = "consent_form"
    INSURANCE_CLAIM = "insurance_claim"
    POLICY_DOCUMENT = "policy_document"
    PATIENT_EDUCATION = "patient_education"


class TranslationStatus(str, Enum):
    """Translation processing status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REQUIRES_REVIEW = "requires_review"


class MedicalTerminology(BaseModel):
    """Medical terminology mapping"""
    
    term_id: str = Field(default_factory=lambda: str(uuid4()))
    
    # Source term
    source_term: str
    source_language: LanguageCode
    
    # Target term
    target_term: str
    target_language: LanguageCode
    
    # Medical coding
    icd10_code: Optional[str] = None
    cpt_code: Optional[str] = None
    snomed_code: Optional[str] = None
    loinc_code: Optional[str] = None
    
    # Context
    specialty: Optional[str] = None
    body_system: Optional[str] = None
    
    # Usage statistics
    usage_count: int = 0
    confidence_score: float = 1.0
    
    # Metadata
    verified: bool = False
    verified_by: Optional[str] = None
    verified_at: Optional[datetime] = None


class QualityMetrics(BaseModel):
    """Translation quality assessment metrics"""
    
    # Completeness
    completeness_score: float = 0.0  # 0-1
    missing_sections: List[str] = Field(default_factory=list)
    
    # Terminology accuracy
    terminology_accuracy: float = 0.0  # 0-1
    terminology_matches: int = 0
    terminology_mismatches: int = 0
    
    # Formatting preservation
    formatting_preserved: bool = True
    formatting_issues: List[str] = Field(default_factory=list)
    
    # Context consistency
    context_consistency: float = 0.0  # 0-1
    context_issues: List[str] = Field(default_factory=list)
    
    # Medical accuracy
    medical_accuracy: float = 0.0  # 0-1
    potential_errors: List[str] = Field(default_factory=list)
    
    # Overall score
    overall_score: float = 0.0  # 0-1
    
    # Pass/Fail
    meets_threshold: bool = False
    threshold_used: float = 0.85


class TranslationRequest(BaseModel):
    """Request for medical translation"""
    
    request_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Source content
    source_text: str
    source_language: LanguageCode
    target_language: LanguageCode
    
    # Document context
    document_type: DocumentType
    medical_specialty: Optional[str] = None
    
    # Patient context (for personalization)
    patient_id: Optional[UUID] = None
    encounter_id: Optional[UUID] = None
    
    # Translation options
    preserve_formatting: bool = True
    include_terminology_glossary: bool = True
    use_formal_tone: bool = True
    
    # Quality requirements
    quality_threshold: float = 0.85
    requires_verification: bool = False
    
    # Cache control
    use_cached_translation: bool = True
    cache_ttl: int = 86400  # 24 hours
    
    # Metadata
    requester_id: Optional[str] = None
    priority: str = "normal"
    metadata: Dict[str, Any] = Field(default_factory=dict)


class TranslationResponse(BaseModel, TimestampMixin):
    """Response from translation service"""
    
    translation_id: UUID = Field(default_factory=uuid4)
    request_id: UUID
    
    # Status
    status: TranslationStatus = TranslationStatus.COMPLETED
    
    # Original and translated content
    source_text: str
    translated_text: str
    source_language: LanguageCode
    target_language: LanguageCode
    
    # Quality assessment
    quality_metrics: QualityMetrics
    
    # Terminology used
    terminology_used: List[MedicalTerminology] = Field(default_factory=list)
    
    # Processing details
    model_used: str = "gpt-4-turbo"
    processing_time_ms: int = 0
    cached: bool = False
    
    # Review status
    requires_review: bool = False
    review_reasons: List[str] = Field(default_factory=list)
    reviewed: bool = False
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    
    # Confidence
    confidence_score: float = 0.0  # 0-1
    
    # Alternative translations (if ambiguous)
    alternatives: List[str] = Field(default_factory=list)
    
    # Warnings and notes
    warnings: List[str] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)


class TranslationReviewRequest(BaseModel):
    """Request for human review of translation"""
    
    translation_id: UUID
    reviewer_id: str
    
    # Review details
    approved: bool
    corrections: Optional[str] = None
    feedback: Optional[str] = None
    
    # Terminology updates
    terminology_additions: List[MedicalTerminology] = Field(default_factory=list)
    terminology_corrections: List[MedicalTerminology] = Field(default_factory=list)
    
    # Quality feedback
    quality_rating: int = Field(ge=1, le=5)  # 1-5 stars
    
    # Timestamp
    reviewed_at: datetime = Field(default_factory=datetime.utcnow)


class BilingualDocument(BaseModel):
    """Bilingual document representation"""
    
    document_id: UUID = Field(default_factory=uuid4)
    document_type: DocumentType
    
    # Content in both languages
    content_en: str
    content_ar: str
    
    # Metadata
    title_en: Optional[str] = None
    title_ar: Optional[str] = None
    
    # Patient/Encounter references
    patient_id: Optional[UUID] = None
    encounter_id: Optional[UUID] = None
    
    # Versioning
    version: int = 1
    translation_id: Optional[UUID] = None
    
    # Audit
    created_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Distribution
    distributed_to_patient: bool = False
    distributed_at: Optional[datetime] = None


class BatchTranslationRequest(BaseModel):
    """Batch translation request for multiple documents"""
    
    batch_id: UUID = Field(default_factory=uuid4)
    requests: List[TranslationRequest]
    
    # Batch options
    parallel_processing: bool = True
    max_concurrent: int = 5
    
    # Callback
    callback_url: Optional[str] = None
    
    # Progress tracking
    progress_webhook: Optional[str] = None


class BatchTranslationResponse(BaseModel):
    """Response for batch translation"""
    
    batch_id: UUID
    total_requests: int
    completed: int = 0
    failed: int = 0
    in_progress: int = 0
    
    # Results
    translations: List[TranslationResponse] = Field(default_factory=list)
    errors: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Timing
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    total_time_seconds: Optional[int] = None
    
    # Status
    status: str = "in_progress"  # pending, in_progress, completed, failed
