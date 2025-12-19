"""
RADIOLINC - Radiology Report Analysis
AI-powered analysis of radiology reports and DICOM metadata
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Dict, Any, List, Optional
from uuid import uuid4

from shared.config.settings import settings
from shared.models.base import HealthCheckResponse
from shared.models.radiology import (
    RadiologyReportRequest,
    RadiologyReportResponse,
    DicomAnalysisRequest,
    DicomAnalysisResponse,
    FindingsExtraction,
    ImagingRecommendation
)
from shared.utils.logger import get_logger
from shared.integrations.n8n_client import N8NClient

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management"""
    logger.info("Starting RADIOLINC")
    yield
    logger.info("Shutting down RADIOLINC")


app = FastAPI(
    title="RADIOLINC - Radiology Analysis",
    description="AI-powered radiology report analysis and DICOM processing",
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs" if settings.api_docs_enabled else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_credentials,
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
)

# Initialize n8n client
n8n_client = N8NClient(settings.n8n.server_url)


@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    return HealthCheckResponse(
        status="healthy",
        version=settings.app_version,
        environment=settings.environment,
    )


@app.post("/api/v1/analyze-report", response_model=RadiologyReportResponse)
async def analyze_radiology_report(request: RadiologyReportRequest):
    """
    Analyze radiology report using AI
    Extracts findings, impressions, and recommendations
    """
    try:
        logger.info(
            "Analyzing radiology report",
            request_id=str(request.request_id),
            modality=request.modality
        )
        
        # Trigger n8n workflow for radiology report analysis
        n8n_response = await n8n_client.trigger_workflow(
            workflow_name="radiology_report_analysis",
            data={
                "request_id": str(request.request_id),
                "patient_id": str(request.patient_id),
                "report_text": request.report_text,
                "modality": request.modality,
                "body_part": request.body_part,
                "extract_findings": True,
                "generate_summary": True,
                "detect_critical_findings": True,
                "bilingual_output": True,
                "use_ai": True,
                "model": settings.openai.model_gpt4
            }
        )
        
        # Parse analysis response
        analysis_data = n8n_response.get("data", {})
        
        return RadiologyReportResponse(
            request_id=request.request_id,
            report_id=str(uuid4()),
            extracted_findings=analysis_data.get("findings", []),
            impression=analysis_data.get("impression", ""),
            critical_findings=analysis_data.get("critical_findings", []),
            structured_report=analysis_data.get("structured_report", {}),
            recommendations=analysis_data.get("recommendations", []),
            follow_up_required=analysis_data.get("follow_up_required", False),
            urgency_level=analysis_data.get("urgency_level", "routine"),
            radlex_codes=analysis_data.get("radlex_codes", []),
            icd10_codes=analysis_data.get("icd10_codes", []),
            confidence_score=analysis_data.get("confidence_score", 0.85),
            summary_en=analysis_data.get("summary_en", ""),
            summary_ar=analysis_data.get("summary_ar", ""),
            ai_model_used=settings.openai.model_gpt4,
            n8n_workflow_id=n8n_response.get("workflow_id")
        )
        
    except Exception as e:
        logger.error("Radiology report analysis failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/analyze-dicom", response_model=DicomAnalysisResponse)
async def analyze_dicom(request: DicomAnalysisRequest):
    """
    Analyze DICOM metadata and images
    Extracts technical parameters and validates quality
    """
    try:
        logger.info(
            "Analyzing DICOM",
            request_id=str(request.request_id),
            study_id=request.study_instance_uid
        )
        
        # Trigger n8n workflow for DICOM analysis
        n8n_response = await n8n_client.trigger_workflow(
            workflow_name="dicom_analysis",
            data={
                "request_id": str(request.request_id),
                "study_uid": request.study_instance_uid,
                "series_uid": request.series_instance_uid,
                "dicom_url": request.dicom_file_url,
                "extract_metadata": True,
                "validate_quality": True,
                "detect_anatomy": True
            }
        )
        
        # Parse DICOM analysis response
        dicom_data = n8n_response.get("data", {})
        
        return DicomAnalysisResponse(
            request_id=request.request_id,
            study_instance_uid=request.study_instance_uid,
            metadata=dicom_data.get("metadata", {}),
            modality=dicom_data.get("modality", ""),
            body_part_examined=dicom_data.get("body_part", ""),
            study_description=dicom_data.get("study_description", ""),
            series_count=dicom_data.get("series_count", 0),
            image_count=dicom_data.get("image_count", 0),
            quality_assessment=dicom_data.get("quality_assessment", {}),
            detected_anatomy=dicom_data.get("detected_anatomy", []),
            technical_issues=dicom_data.get("technical_issues", []),
            n8n_workflow_id=n8n_response.get("workflow_id")
        )
        
    except Exception as e:
        logger.error("DICOM analysis failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/upload-dicom")
async def upload_dicom_file(file: UploadFile = File(...)):
    """
    Upload DICOM file for analysis
    """
    try:
        # Read file content
        content = await file.read()
        
        # Trigger n8n workflow for DICOM upload
        n8n_response = await n8n_client.trigger_workflow(
            workflow_name="dicom_upload",
            data={
                "filename": file.filename,
                "content_type": file.content_type,
                "size_bytes": len(content)
            },
            files={"dicom_file": (file.filename, content, file.content_type)}
        )
        
        return {
            "status": "uploaded",
            "file_id": n8n_response.get("data", {}).get("file_id"),
            "n8n_workflow_id": n8n_response.get("workflow_id"),
            "message": "DICOM file uploaded successfully"
        }
        
    except Exception as e:
        logger.error("DICOM upload failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/compare-studies")
async def compare_radiology_studies(
    previous_study_id: str,
    current_study_id: str
) -> Dict[str, Any]:
    """
    Compare two radiology studies to detect changes
    """
    try:
        # Trigger n8n workflow for study comparison
        n8n_response = await n8n_client.trigger_workflow(
            workflow_name="radiology_study_comparison",
            data={
                "previous_study_id": previous_study_id,
                "current_study_id": current_study_id,
                "detect_progression": True,
                "highlight_changes": True,
                "use_ai": True
            }
        )
        
        return n8n_response.get("data", {})
        
    except Exception as e:
        logger.error("Study comparison failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "RADIOLINC",
        "description": "Radiology Report Analysis",
        "version": settings.app_version,
        "features": [
            "AI-powered report analysis",
            "DICOM metadata extraction",
            "Critical findings detection",
            "Study comparison",
            "RadLex & ICD-10 coding",
            "Bilingual support",
            "n8n automation integration"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.agents.radiolinc_port,
        reload=settings.debug
    )
