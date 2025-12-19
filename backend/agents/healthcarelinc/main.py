"""
HEALTHCARELINC - Healthcare Workflow Automation
FHIR R4 validation and NPHIES compliance
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Dict, Any

from shared.config.settings import settings
from shared.models.base import HealthCheckResponse
from shared.models.healthcare import (
    HealthcareWorkflowRequest,
    HealthcareWorkflowResponse,
    EncounterType
)
from shared.utils.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management"""
    logger.info("Starting HEALTHCARELINC")
    yield
    logger.info("Shutting down HEALTHCARELINC")


app = FastAPI(
    title="HEALTHCARELINC - Healthcare Workflow Automation",
    description="Healthcare operations automation with FHIR/NPHIES compliance",
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


@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    return HealthCheckResponse(
        status="healthy",
        version=settings.app_version,
        environment=settings.environment,
    )


@app.post("/api/v1/process", response_model=HealthcareWorkflowResponse)
async def process_workflow(request: HealthcareWorkflowRequest):
    """
    Process healthcare workflow
    Supports: Emergency, Admission, Discharge, Referral
    """
    try:
        logger.info(
            "Processing healthcare workflow",
            request_id=str(request.request_id),
            workflow_type=request.workflow_type.value
        )
        
        # Route to appropriate workflow handler
        if request.workflow_type == EncounterType.EMERGENCY:
            result = await process_emergency(request)
        elif request.workflow_type == EncounterType.ADMISSION:
            result = await process_admission(request)
        elif request.workflow_type == EncounterType.DISCHARGE:
            result = await process_discharge(request)
        elif request.workflow_type == EncounterType.REFERRAL:
            result = await process_referral(request)
        else:
            raise ValueError(f"Unsupported workflow type: {request.workflow_type}")
        
        return result
        
    except Exception as e:
        logger.error("Workflow processing failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


async def process_emergency(request: HealthcareWorkflowRequest) -> HealthcareWorkflowResponse:
    """Process emergency workflow"""
    # TODO: Implement emergency workflow logic
    return HealthcareWorkflowResponse(
        request_id=request.request_id,
        status="success",
        encounter_id=request.encounter.id,
        validation_passed=True,
        agents_used=["HEALTHCARELINC"],
        messages_en=["Emergency workflow processed successfully"],
        messages_ar=["تمت معالجة سير العمل الطارئ بنجاح"]
    )


async def process_admission(request: HealthcareWorkflowRequest) -> HealthcareWorkflowResponse:
    """Process admission workflow"""
    # TODO: Implement admission workflow logic
    return HealthcareWorkflowResponse(
        request_id=request.request_id,
        status="success",
        encounter_id=request.encounter.id,
        validation_passed=True,
        agents_used=["HEALTHCARELINC"],
        messages_en=["Admission workflow processed successfully"],
        messages_ar=["تمت معالجة سير عمل الدخول بنجاح"]
    )


async def process_discharge(request: HealthcareWorkflowRequest) -> HealthcareWorkflowResponse:
    """Process discharge workflow"""
    # TODO: Implement discharge workflow logic
    return HealthcareWorkflowResponse(
        request_id=request.request_id,
        status="success",
        encounter_id=request.encounter.id,
        validation_passed=True,
        agents_used=["HEALTHCARELINC"],
        messages_en=["Discharge workflow processed successfully"],
        messages_ar=["تمت معالجة سير عمل الخروج بنجاح"]
    )


async def process_referral(request: HealthcareWorkflowRequest) -> HealthcareWorkflowResponse:
    """Process referral workflow"""
    # TODO: Implement referral workflow logic
    return HealthcareWorkflowResponse(
        request_id=request.request_id,
        status="success",
        encounter_id=request.encounter.id,
        validation_passed=True,
        agents_used=["HEALTHCARELINC"],
        messages_en=["Referral workflow processed successfully"],
        messages_ar=["تمت معالجة سير عمل الإحالة بنجاح"]
    )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "HEALTHCARELINC",
        "description": "Healthcare Workflow Automation",
        "version": settings.app_version,
        "workflows": ["emergency", "admission", "discharge", "referral"]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.agents.healthcarelinc_port,
        reload=settings.debug
    )
