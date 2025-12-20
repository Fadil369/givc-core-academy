"""
Healthcare domain models - FHIR R4 compatible
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from uuid import UUID, uuid4

from pydantic import Field

from .base import BaseModel, TimestampMixin, LanguageCode


class Gender(str, Enum):
    """Patient gender"""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNKNOWN = "unknown"


class EncounterStatus(str, Enum):
    """Encounter status"""
    PLANNED = "planned"
    ARRIVED = "arrived"
    TRIAGED = "triaged"
    IN_PROGRESS = "in-progress"
    ON_LEAVE = "onleave"
    FINISHED = "finished"
    CANCELLED = "cancelled"


class EncounterType(str, Enum):
    """Types of healthcare encounters"""
    EMERGENCY = "emergency"
    ADMISSION = "admission"
    DISCHARGE = "discharge"
    REFERRAL = "referral"
    OUTPATIENT = "outpatient"
    INPATIENT = "inpatient"


class CodeableConcept(BaseModel):
    """FHIR CodeableConcept"""
    
    coding: List[Dict[str, Any]] = Field(default_factory=list)
    text: Optional[str] = None
    
    @classmethod
    def from_code(cls, system: str, code: str, display: str):
        """Create from code"""
        return cls(
            coding=[{
                "system": system,
                "code": code,
                "display": display
            }],
            text=display
        )


class Identifier(BaseModel):
    """FHIR Identifier"""
    
    system: str
    value: str
    use: Optional[str] = None
    type: Optional[CodeableConcept] = None


class HumanName(BaseModel):
    """FHIR HumanName"""
    
    use: str = "official"
    text: Optional[str] = None
    family: Optional[str] = None
    given: List[str] = Field(default_factory=list)
    prefix: List[str] = Field(default_factory=list)
    suffix: List[str] = Field(default_factory=list)


class Address(BaseModel):
    """FHIR Address"""
    
    use: str = "home"
    type: str = "physical"
    text: Optional[str] = None
    line: List[str] = Field(default_factory=list)
    city: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: str = "SA"  # Saudi Arabia


class ContactPoint(BaseModel):
    """FHIR ContactPoint"""
    
    system: str  # phone, email, fax
    value: str
    use: Optional[str] = None
    rank: Optional[int] = None


class Patient(TimestampMixin):
    """Patient resource - FHIR R4 compatible"""
    
    id: UUID = Field(default_factory=uuid4)
    identifier: List[Identifier] = Field(default_factory=list)
    
    # Demographics
    name: List[HumanName] = Field(default_factory=list)
    gender: Gender
    birth_date: datetime
    deceased: bool = False
    deceased_datetime: Optional[datetime] = None
    
    # Contact
    telecom: List[ContactPoint] = Field(default_factory=list)
    address: List[Address] = Field(default_factory=list)
    
    # Communication
    language: LanguageCode = LanguageCode.ARABIC
    
    # Saudi-specific
    national_id: Optional[str] = None  # Saudi National ID
    iqama_number: Optional[str] = None  # Resident ID
    
    # Insurance
    insurance_member_id: Optional[str] = None
    payer_id: Optional[str] = None
    
    # Metadata
    active: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Encounter(TimestampMixin):
    """Encounter resource - Healthcare interaction"""
    
    id: UUID = Field(default_factory=uuid4)
    identifier: List[Identifier] = Field(default_factory=list)
    
    # Status and type
    status: EncounterStatus
    encounter_type: EncounterType
    
    # Patient reference
    patient_id: UUID
    patient: Optional[Patient] = None
    
    # Period
    period_start: datetime
    period_end: Optional[datetime] = None
    
    # Location
    facility_id: str
    facility_name: str
    location: Optional[str] = None
    department: Optional[str] = None
    
    # Clinical
    reason_code: List[CodeableConcept] = Field(default_factory=list)
    diagnosis: List[CodeableConcept] = Field(default_factory=list)
    
    # Priority
    priority: Optional[CodeableConcept] = None
    
    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Observation(TimestampMixin):
    """Observation resource - Clinical findings"""
    
    id: UUID = Field(default_factory=uuid4)
    
    # Status
    status: str = "final"  # registered, preliminary, final, amended
    
    # References
    patient_id: UUID
    encounter_id: Optional[UUID] = None
    
    # Category and code
    category: List[CodeableConcept] = Field(default_factory=list)
    code: CodeableConcept  # LOINC code
    
    # Value
    value_quantity: Optional[Dict[str, Any]] = None
    value_string: Optional[str] = None
    value_boolean: Optional[bool] = None
    
    # Interpretation
    interpretation: Optional[CodeableConcept] = None
    
    # Time
    effective_datetime: datetime = Field(default_factory=datetime.utcnow)
    
    # Bilingual
    note_ar: Optional[str] = None
    note_en: Optional[str] = None


class MedicationRequest(TimestampMixin):
    """Medication request/prescription"""
    
    id: UUID = Field(default_factory=uuid4)
    
    # Status
    status: str = "active"  # active, completed, cancelled
    intent: str = "order"  # proposal, plan, order
    
    # References
    patient_id: UUID
    encounter_id: Optional[UUID] = None
    
    # Medication
    medication_code: CodeableConcept
    
    # Dosage
    dosage_instruction: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Dispense
    dispense_request: Optional[Dict[str, Any]] = None
    
    # Provider
    requester_id: Optional[str] = None
    
    # Bilingual notes
    note_ar: Optional[str] = None
    note_en: Optional[str] = None


class DiagnosticReport(TimestampMixin):
    """Diagnostic report - Lab results, imaging reports"""
    
    id: UUID = Field(default_factory=uuid4)
    
    # Status
    status: str = "final"  # registered, partial, preliminary, final
    
    # References
    patient_id: UUID
    encounter_id: Optional[UUID] = None
    
    # Category and code
    category: List[CodeableConcept] = Field(default_factory=list)
    code: CodeableConcept
    
    # Results
    result: List[UUID] = Field(default_factory=list)  # Observation IDs
    
    # Conclusion
    conclusion: Optional[str] = None
    conclusion_code: List[CodeableConcept] = Field(default_factory=list)
    
    # Performer
    performer_id: Optional[str] = None
    
    # Time
    effective_datetime: datetime = Field(default_factory=datetime.utcnow)
    issued: datetime = Field(default_factory=datetime.utcnow)
    
    # Bilingual
    conclusion_ar: Optional[str] = None
    conclusion_en: Optional[str] = None


class HealthcareWorkflowRequest(BaseModel):
    """Request for healthcare workflow processing"""
    
    request_id: UUID = Field(default_factory=uuid4)
    workflow_type: EncounterType
    
    # Patient data
    patient: Patient
    
    # Encounter data
    encounter: Encounter
    
    # Additional clinical data
    observations: List[Observation] = Field(default_factory=list)
    medications: List[MedicationRequest] = Field(default_factory=list)
    diagnostic_reports: List[DiagnosticReport] = Field(default_factory=list)
    
    # Processing options
    fhir_validation: bool = True
    nphies_submission: bool = False
    translation_required: bool = False
    
    # Metadata
    priority: str = "normal"
    metadata: Dict[str, Any] = Field(default_factory=dict)


class HealthcareWorkflowResponse(BaseModel):
    """Response from healthcare workflow processing"""
    
    request_id: UUID
    status: str  # success, failed, partial
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Results
    encounter_id: UUID
    fhir_bundle: Optional[Dict[str, Any]] = None
    nphies_response: Optional[Dict[str, Any]] = None
    
    # Validation results
    validation_passed: bool = True
    validation_errors: List[str] = Field(default_factory=list)
    
    # Processing details
    processing_time_ms: int = 0
    agents_used: List[str] = Field(default_factory=list)
    
    # Bilingual support
    messages_ar: List[str] = Field(default_factory=list)
    messages_en: List[str] = Field(default_factory=list)
