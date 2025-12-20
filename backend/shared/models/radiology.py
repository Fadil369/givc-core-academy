"""
Radiology models for RADIOLINC
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from uuid import UUID, uuid4

from pydantic import Field

from .base import BaseModel, TimestampMixin


class ImagingModality(str, Enum):
    """Radiology imaging modalities"""
    CT = "CT"
    MRI = "MRI"
    XRAY = "XRAY"
    ULTRASOUND = "ULTRASOUND"
    MAMMOGRAPHY = "MAMMOGRAPHY"
    PET = "PET"
    NUCLEAR = "NUCLEAR"


class RadiologyReportRequest(BaseModel):
    """Request for radiology report analysis"""
    
    request_id: UUID = Field(default_factory=uuid4)
    patient_id: UUID
    report_text: str
    modality: ImagingModality
    body_part: str
    study_date: datetime = Field(default_factory=datetime.utcnow)


class RadiologyReportResponse(TimestampMixin):
    """Response from radiology report analysis"""
    
    request_id: UUID
    report_id: str
    extracted_findings: List[Dict[str, Any]] = Field(default_factory=list)
    impression: str
    critical_findings: List[str] = Field(default_factory=list)
    structured_report: Dict[str, Any] = Field(default_factory=dict)
    recommendations: List[str] = Field(default_factory=list)
    follow_up_required: bool
    urgency_level: str
    radlex_codes: List[str] = Field(default_factory=list)
    icd10_codes: List[str] = Field(default_factory=list)
    confidence_score: float
    summary_en: str
    summary_ar: str
    ai_model_used: str
    n8n_workflow_id: Optional[str] = None


class DicomAnalysisRequest(BaseModel):
    """Request for DICOM analysis"""
    
    request_id: UUID = Field(default_factory=uuid4)
    study_instance_uid: str
    series_instance_uid: Optional[str] = None
    dicom_file_url: Optional[str] = None


class DicomAnalysisResponse(TimestampMixin):
    """Response from DICOM analysis"""
    
    request_id: UUID
    study_instance_uid: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    modality: str
    body_part_examined: str
    study_description: str
    series_count: int
    image_count: int
    quality_assessment: Dict[str, Any] = Field(default_factory=dict)
    detected_anatomy: List[str] = Field(default_factory=list)
    technical_issues: List[str] = Field(default_factory=list)
    n8n_workflow_id: Optional[str] = None


class FindingsExtraction(BaseModel):
    """Extracted finding from radiology report"""
    
    finding: str
    location: str
    severity: Optional[str] = None
    measurement: Optional[str] = None


class ImagingRecommendation(BaseModel):
    """Imaging recommendation"""
    
    modality: ImagingModality
    reason: str
    urgency: str
    body_part: str
