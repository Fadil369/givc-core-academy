"""
Policy models for POLICYLINC
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from uuid import UUID, uuid4

from pydantic import Field

from .base import BaseModel, TimestampMixin


class PolicyType(str, Enum):
    """Insurance policy types"""
    MEDICAL = "medical"
    DENTAL = "dental"
    VISION = "vision"
    PHARMACY = "pharmacy"
    MENTAL_HEALTH = "mental_health"


class CoverageRule(BaseModel):
    """Insurance coverage rule"""
    
    rule_id: str = Field(default_factory=lambda: str(uuid4()))
    rule_name: str
    service_codes: List[str] = Field(default_factory=list)
    coverage_percentage: float
    conditions: List[str] = Field(default_factory=list)
    exclusions: List[str] = Field(default_factory=list)
    requires_prior_auth: bool = False


class PolicyDocument(TimestampMixin):
    """Insurance policy document"""
    
    document_id: UUID = Field(default_factory=uuid4)
    payer_id: str
    payer_name: str
    policy_type: PolicyType
    document_url: Optional[str] = None
    document_text: Optional[str] = None
    effective_date: datetime
    expiration_date: Optional[datetime] = None
    version: str = "1.0"


class PolicyInterpretationRequest(BaseModel):
    """Request for policy interpretation"""
    
    request_id: UUID = Field(default_factory=uuid4)
    payer_id: str
    policy_type: PolicyType
    policy_text: str
    specific_questions: List[str] = Field(default_factory=list)


class PolicyInterpretationResponse(TimestampMixin):
    """Response from policy interpretation"""
    
    request_id: UUID
    policy_id: str
    payer_id: str
    interpretation_summary: str
    coverage_rules: List[CoverageRule] = Field(default_factory=list)
    exclusions: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    prior_authorization_required: List[str] = Field(default_factory=list)
    confidence_score: float
    ai_model_used: str
    interpretation_en: str
    interpretation_ar: str
    n8n_workflow_id: Optional[str] = None


class CoverageCheckRequest(BaseModel):
    """Request to check coverage"""
    
    request_id: UUID = Field(default_factory=uuid4)
    payer_id: str
    patient_id: UUID
    procedure_code: str
    diagnosis_codes: List[str] = Field(default_factory=list)


class CoverageCheckResponse(TimestampMixin):
    """Response from coverage check"""
    
    request_id: UUID
    is_covered: bool
    coverage_percentage: float
    patient_responsibility: float
    prior_authorization_required: bool
    coverage_details: str
    applicable_rules: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    n8n_workflow_id: Optional[str] = None
