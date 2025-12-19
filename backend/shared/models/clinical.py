"""
Clinical models for CLINICALLINC
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from uuid import UUID, uuid4

from pydantic import Field

from .base import BaseModel, TimestampMixin


class UrgencyLevel(str, Enum):
    """Clinical urgency levels"""
    CRITICAL = "critical"
    URGENT = "urgent"
    SEMI_URGENT = "semi_urgent"
    ROUTINE = "routine"


class ClinicalDecisionRequest(BaseModel):
    """Request for clinical decision support"""
    
    request_id: UUID = Field(default_factory=uuid4)
    patient_id: UUID
    chief_complaint: str
    symptoms: List[str] = Field(default_factory=list)
    vital_signs: Dict[str, Any] = Field(default_factory=dict)
    lab_results: Dict[str, Any] = Field(default_factory=dict)
    medical_history: List[str] = Field(default_factory=list)
    current_medications: List[str] = Field(default_factory=list)


class ClinicalDecisionResponse(BaseModel, TimestampMixin):
    """Response from clinical decision support"""
    
    request_id: UUID
    differential_diagnosis: List[Dict[str, Any]] = Field(default_factory=list)
    recommended_tests: List[str] = Field(default_factory=list)
    treatment_recommendations: List[str] = Field(default_factory=list)
    red_flags: List[str] = Field(default_factory=list)
    urgency_level: UrgencyLevel
    confidence_score: float
    clinical_notes: str
    evidence_based_guidelines: List[str] = Field(default_factory=list)
    ai_model_used: str
    n8n_workflow_id: Optional[str] = None


class DrugInteractionCheck(BaseModel):
    """Request to check drug interactions"""
    
    request_id: UUID = Field(default_factory=uuid4)
    patient_id: Optional[UUID] = None
    medications: List[str]


class DrugInteractionResponse(BaseModel, TimestampMixin):
    """Response from drug interaction check"""
    
    request_id: UUID
    has_interactions: bool
    interactions: List[Dict[str, Any]] = Field(default_factory=list)
    severity_summary: Dict[str, int] = Field(default_factory=dict)
    recommendations: List[str] = Field(default_factory=list)
    contraindications: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    safe_to_prescribe: bool
    n8n_workflow_id: Optional[str] = None


class CarePathwayRequest(BaseModel):
    """Request for care pathway"""
    
    request_id: UUID = Field(default_factory=uuid4)
    patient_id: UUID
    condition: str
    severity: str
    patient_age: int
    comorbidities: List[str] = Field(default_factory=list)


class CarePathwayResponse(BaseModel, TimestampMixin):
    """Response with care pathway"""
    
    request_id: UUID
    condition: str
    pathway_steps: List[Dict[str, Any]] = Field(default_factory=list)
    medications: List[str] = Field(default_factory=list)
    monitoring_parameters: List[str] = Field(default_factory=list)
    expected_outcomes: List[str] = Field(default_factory=list)
    red_flags: List[str] = Field(default_factory=list)
    follow_up_schedule: List[str] = Field(default_factory=list)
    evidence_level: str
    guidelines_reference: List[str] = Field(default_factory=list)
    pathway_en: str
    pathway_ar: str
    n8n_workflow_id: Optional[str] = None


class DiagnosticSuggestion(BaseModel):
    """Diagnostic suggestion"""
    
    diagnosis: str
    icd10_code: str
    probability: float
    supporting_findings: List[str] = Field(default_factory=list)
    recommended_tests: List[str] = Field(default_factory=list)
