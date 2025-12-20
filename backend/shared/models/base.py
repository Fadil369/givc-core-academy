"""
Base Pydantic models for all BrainSAIT LINC agents
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel as PydanticBaseModel, Field, ConfigDict


class BaseModel(PydanticBaseModel):
    """Base model with common configuration"""
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        json_encoders={
            datetime: lambda v: v.isoformat(),
        }
    )


class TimestampMixin(BaseModel):
    """Mixin for timestamp fields"""
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None


class PriorityLevel(str, Enum):
    """Request priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    NORMAL = "normal"
    LOW = "low"


class AgentType(str, Enum):
    """Available LINC agent types"""
    MASTERLINC = "MASTERLINC"
    HEALTHCARELINC = "HEALTHCARELINC"
    CLAIMLINC = "CLAIMLINC"
    POLICYLINC = "POLICYLINC"
    CLINICALLINC = "CLINICALLINC"
    TTLINC = "TTLINC"
    RADIOLINC = "RADIOLINC"
    COMPLIANCELINC = "COMPLIANCELINC"


class LanguageCode(str, Enum):
    """Supported language codes"""
    ARABIC = "ar"
    ENGLISH = "en"


class OrchestrationContext(BaseModel):
    """Context passed between agents via MASTERLINC"""
    
    request_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source: str = "api"
    priority: PriorityLevel = PriorityLevel.NORMAL
    
    # Agent routing
    agent_type: AgentType
    agents_chain: List[AgentType] = Field(default_factory=list)
    
    # Compliance
    hipaa_enabled: bool = True
    nphies_enabled: bool = True
    audit_required: bool = True
    
    # Bilingual support
    primary_language: LanguageCode = LanguageCode.ENGLISH
    secondary_language: Optional[LanguageCode] = LanguageCode.ARABIC
    translation_required: bool = False
    
    # User context
    user_id: Optional[str] = None
    organization_id: Optional[str] = None
    facility_id: Optional[str] = None
    
    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def add_agent_to_chain(self, agent: AgentType) -> None:
        """Add agent to processing chain"""
        if agent not in self.agents_chain:
            self.agents_chain.append(agent)


class HealthCheckResponse(BaseModel):
    """Standard health check response"""
    
    status: str = "healthy"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str
    environment: str
    
    # Service checks
    database: bool = True
    redis: bool = True
    external_apis: Dict[str, bool] = Field(default_factory=dict)
    
    # Metrics
    uptime_seconds: int = 0
    requests_total: int = 0
    requests_failed: int = 0
    
    @property
    def is_healthy(self) -> bool:
        """Check if all services are healthy"""
        return (
            self.status == "healthy" and
            self.database and
            self.redis and
            all(self.external_apis.values())
        )


class ErrorDetail(BaseModel):
    """Detailed error information"""
    
    code: str
    message: str
    field: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """Standard error response"""
    
    error: str
    message: str
    details: List[ErrorDetail] = Field(default_factory=list)
    request_id: Optional[UUID] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # HIPAA compliance - never expose PHI in errors
    phi_redacted: bool = True


class PaginationParams(BaseModel):
    """Standard pagination parameters"""
    
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    
    @property
    def skip(self) -> int:
        """Calculate skip value for database queries"""
        return (self.page - 1) * self.page_size


class PaginatedResponse(BaseModel):
    """Paginated response wrapper"""
    
    items: List[Any]
    total: int
    page: int
    page_size: int
    total_pages: int
    
    @classmethod
    def create(cls, items: List[Any], total: int, params: PaginationParams):
        """Create paginated response"""
        total_pages = (total + params.page_size - 1) // params.page_size
        return cls(
            items=items,
            total=total,
            page=params.page,
            page_size=params.page_size,
            total_pages=total_pages
        )


class AuditLog(TimestampMixin):
    """Audit log entry for HIPAA compliance"""
    
    id: UUID = Field(default_factory=uuid4)
    event_type: str
    user_id: Optional[str]
    organization_id: Optional[str]
    resource_type: str
    resource_id: str
    action: str  # CREATE, READ, UPDATE, DELETE
    phi_accessed: bool = False
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    success: bool = True
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ComplianceFlags(BaseModel):
    """Compliance and regulatory flags"""
    
    hipaa_compliant: bool = True
    nphies_compliant: bool = True
    moh_compliant: bool = True
    gdpr_compliant: bool = False
    
    # Data handling
    contains_phi: bool = False
    phi_encrypted: bool = False
    audit_logged: bool = False
    
    # Validation
    fhir_validated: bool = False
    icd10_validated: bool = False
    cpt_validated: bool = False
