"""
Claims processing models - NPHIES compatible
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from uuid import UUID, uuid4
from decimal import Decimal

from pydantic import Field

from .base import BaseModel, TimestampMixin, LanguageCode


class ClaimStatus(str, Enum):
    """Claim status"""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    PARTIAL = "partial"
    APPEALED = "appealed"


class ClaimType(str, Enum):
    """Claim type"""
    INSTITUTIONAL = "institutional"
    ORAL = "oral"
    PHARMACY = "pharmacy"
    PROFESSIONAL = "professional"
    VISION = "vision"


class RejectionSeverity(str, Enum):
    """Rejection severity level"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RejectionCode(BaseModel):
    """NPHIES rejection code"""
    
    code: str
    system: str = "http://nphies.sa/terminology/rejection-reason"
    display: str
    display_ar: Optional[str] = None
    severity: RejectionSeverity = RejectionSeverity.MEDIUM
    
    # Resolution guidance
    resolution_guidance_en: Optional[str] = None
    resolution_guidance_ar: Optional[str] = None
    
    # Automation
    auto_correctable: bool = False
    requires_manual_review: bool = True
    
    # Common issues
    common_causes: List[str] = Field(default_factory=list)
    related_codes: List[str] = Field(default_factory=list)


class ClaimItem(BaseModel):
    """Individual claim line item"""
    
    sequence: int
    
    # Service
    service_code: str
    service_system: str = "http://nphies.sa/terminology/service-code"
    service_display: str
    service_display_ar: Optional[str] = None
    
    # Quantity and pricing
    quantity: int = 1
    unit_price: Decimal
    net_amount: Decimal
    
    # Modifiers
    modifiers: List[str] = Field(default_factory=list)
    
    # Diagnosis
    diagnosis_sequence: List[int] = Field(default_factory=list)
    
    # Provider
    provider_id: Optional[str] = None
    
    # Dates
    serviced_date: datetime
    
    # Status
    rejected: bool = False
    rejection_reason: Optional[RejectionCode] = None


class Diagnosis(BaseModel):
    """Claim diagnosis"""
    
    sequence: int
    
    # ICD-10 code
    diagnosis_code: str
    diagnosis_system: str = "http://hl7.org/fhir/sid/icd-10"
    diagnosis_display: str
    diagnosis_display_ar: Optional[str] = None
    
    # Type
    type: str = "principal"  # principal, admitting, discharge
    
    # On admission indicator
    on_admission: Optional[bool] = None


class Claim(BaseModel, TimestampMixin):
    """Healthcare claim - NPHIES compatible"""
    
    id: UUID = Field(default_factory=uuid4)
    
    # Identifiers
    claim_id: str  # Provider's claim ID
    nphies_claim_id: Optional[str] = None  # NPHIES assigned ID
    
    # Status and type
    status: ClaimStatus = ClaimStatus.DRAFT
    claim_type: ClaimType
    
    # Patient
    patient_id: UUID
    member_id: str  # Insurance member ID
    
    # Payer
    payer_id: str
    payer_name: str
    
    # Provider
    provider_id: str
    provider_name: str
    facility_id: Optional[str] = None
    
    # Dates
    service_start_date: datetime
    service_end_date: datetime
    billable_period_start: datetime
    billable_period_end: datetime
    
    # Encounter
    encounter_id: Optional[UUID] = None
    
    # Clinical
    diagnoses: List[Diagnosis] = Field(default_factory=list)
    items: List[ClaimItem] = Field(default_factory=list)
    
    # Financial
    total_gross: Decimal = Decimal("0.00")
    total_net: Decimal = Decimal("0.00")
    total_patient_share: Decimal = Decimal("0.00")
    total_payer_share: Decimal = Decimal("0.00")
    
    # Priority
    priority: str = "normal"  # stat, normal
    
    # Supporting info
    supporting_info: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Processing
    submission_count: int = 0
    last_submitted_at: Optional[datetime] = None
    
    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ClaimResponse(BaseModel, TimestampMixin):
    """Response from payer for a claim"""
    
    id: UUID = Field(default_factory=uuid4)
    
    # References
    claim_id: UUID
    nphies_response_id: Optional[str] = None
    
    # Status
    status: str  # active, cancelled, draft, entered-in-error
    outcome: str  # queued, complete, error, partial
    
    # Disposition
    disposition: Optional[str] = None
    
    # Financial
    payment_amount: Optional[Decimal] = None
    payment_date: Optional[datetime] = None
    
    # Adjudication
    total_approved: Decimal = Decimal("0.00")
    total_rejected: Decimal = Decimal("0.00")
    total_patient_liability: Decimal = Decimal("0.00")
    
    # Items
    item_responses: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Errors
    errors: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Processing
    response_time_ms: int = 0
    processed_at: datetime = Field(default_factory=datetime.utcnow)


class ClaimAnalysis(BaseModel):
    """AI-powered claim analysis result"""
    
    claim_id: UUID
    analysis_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Overall assessment
    confidence_score: float = 0.0  # 0-1
    automation_available: bool = False
    manual_review_required: bool = True
    
    # Rejection analysis
    rejection_codes: List[RejectionCode] = Field(default_factory=list)
    root_causes: List[str] = Field(default_factory=list)
    
    # Corrections suggested
    suggested_corrections: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Coding recommendations
    diagnosis_corrections: List[Dict[str, Any]] = Field(default_factory=list)
    service_code_corrections: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Financial impact
    potential_recovery_amount: Decimal = Decimal("0.00")
    estimated_approval_probability: float = 0.0
    
    # Processing
    ai_model_used: str = "gpt-4"
    processing_time_ms: int = 0
    
    # Bilingual recommendations
    recommendations_en: List[str] = Field(default_factory=list)
    recommendations_ar: List[str] = Field(default_factory=list)
    
    # Next actions
    next_actions: List[str] = Field(default_factory=list)
    requires_jira_ticket: bool = False
    estimated_resolution_time_hours: int = 0


class ClaimAnalysisRequest(BaseModel):
    """Request for claim analysis"""
    
    claim: Claim
    claim_response: Optional[ClaimResponse] = None
    
    # Analysis options
    include_ai_recommendations: bool = True
    include_coding_suggestions: bool = True
    check_payer_policies: bool = True
    
    # Context
    previous_submissions: List[UUID] = Field(default_factory=list)
    historical_success_rate: Optional[float] = None
    
    # Language
    response_language: LanguageCode = LanguageCode.ENGLISH


class ClaimResubmissionRequest(BaseModel):
    """Request to resubmit a corrected claim"""
    
    original_claim_id: UUID
    corrected_claim: Claim
    analysis_id: UUID
    
    # Corrections applied
    corrections_applied: List[str] = Field(default_factory=list)
    
    # Appeal information
    is_appeal: bool = False
    appeal_justification: Optional[str] = None
    appeal_justification_ar: Optional[str] = None
    
    # Approval
    approved_by: Optional[str] = None
    approval_timestamp: Optional[datetime] = None
