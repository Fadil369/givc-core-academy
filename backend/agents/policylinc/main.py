"""
POLICYLINC - Payer Policy Interpretation
AI-powered interpretation of insurance payer policies and coverage rules
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Dict, Any, List, Optional
from datetime import datetime
from uuid import UUID, uuid4

from shared.config.settings import settings
from shared.models.base import HealthCheckResponse
from shared.models.policy import (
    PolicyInterpretationRequest,
    PolicyInterpretationResponse,
    CoverageCheckRequest,
    CoverageCheckResponse,
    PolicyDocument,
    CoverageRule
)
from shared.utils.logger import get_logger
from shared.integrations.n8n_client import N8NClient

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management"""
    logger.info("Starting POLICYLINC")
    yield
    logger.info("Shutting down POLICYLINC")


app = FastAPI(
    title="POLICYLINC - Payer Policy Interpretation",
    description="AI-powered insurance policy interpretation and coverage analysis",
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


@app.post("/api/v1/interpret-policy", response_model=PolicyInterpretationResponse)
async def interpret_policy(request: PolicyInterpretationRequest):
    """
    Interpret insurance payer policy using AI
    Analyzes policy documents and extracts coverage rules
    """
    try:
        logger.info(
            "Interpreting policy",
            request_id=str(request.request_id),
            payer_id=request.payer_id,
            policy_type=request.policy_type
        )
        
        # Trigger n8n workflow for policy interpretation
        n8n_response = await n8n_client.trigger_workflow(
            workflow_name="policy_interpretation",
            data={
                "request_id": str(request.request_id),
                "payer_id": request.payer_id,
                "policy_type": request.policy_type,
                "policy_text": request.policy_text,
                "use_ai": True,
                "model": settings.openai.model_gpt4
            }
        )
        
        # Parse AI response
        interpretation = await parse_policy_interpretation(n8n_response)
        
        return PolicyInterpretationResponse(
            request_id=request.request_id,
            policy_id=str(uuid4()),
            payer_id=request.payer_id,
            interpretation_summary=interpretation.get("summary", ""),
            coverage_rules=interpretation.get("coverage_rules", []),
            exclusions=interpretation.get("exclusions", []),
            limitations=interpretation.get("limitations", []),
            prior_authorization_required=interpretation.get("prior_auth", []),
            confidence_score=interpretation.get("confidence", 0.85),
            ai_model_used=settings.openai.model_gpt4,
            interpretation_en=interpretation.get("interpretation_en", ""),
            interpretation_ar=interpretation.get("interpretation_ar", "")
        )
        
    except Exception as e:
        logger.error("Policy interpretation failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/check-coverage", response_model=CoverageCheckResponse)
async def check_coverage(request: CoverageCheckRequest):
    """
    Check if a procedure/service is covered under a specific policy
    Real-time coverage verification
    """
    try:
        logger.info(
            "Checking coverage",
            request_id=str(request.request_id),
            payer_id=request.payer_id,
            procedure_code=request.procedure_code
        )
        
        # Trigger n8n workflow for coverage check
        n8n_response = await n8n_client.trigger_workflow(
            workflow_name="coverage_check",
            data={
                "request_id": str(request.request_id),
                "payer_id": request.payer_id,
                "patient_id": str(request.patient_id),
                "procedure_code": request.procedure_code,
                "diagnosis_codes": request.diagnosis_codes,
                "check_prior_auth": True
            }
        )
        
        # Parse coverage response
        coverage_data = n8n_response.get("data", {})
        
        return CoverageCheckResponse(
            request_id=request.request_id,
            is_covered=coverage_data.get("is_covered", False),
            coverage_percentage=coverage_data.get("coverage_percentage", 0),
            patient_responsibility=coverage_data.get("patient_responsibility", 0),
            prior_authorization_required=coverage_data.get("prior_auth_required", False),
            coverage_details=coverage_data.get("details", ""),
            applicable_rules=coverage_data.get("rules", []),
            warnings=coverage_data.get("warnings", []),
            n8n_workflow_id=n8n_response.get("workflow_id")
        )
        
    except Exception as e:
        logger.error("Coverage check failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/analyze-policy-document")
async def analyze_policy_document(document: PolicyDocument):
    """
    Analyze a complete policy document
    Extracts all coverage rules, exclusions, and requirements
    """
    try:
        logger.info(
            "Analyzing policy document",
            document_id=str(document.document_id),
            payer_id=document.payer_id
        )
        
        # Trigger n8n workflow for document analysis
        n8n_response = await n8n_client.trigger_workflow(
            workflow_name="policy_document_analysis",
            data={
                "document_id": str(document.document_id),
                "payer_id": document.payer_id,
                "document_url": document.document_url,
                "document_text": document.document_text,
                "analysis_type": "comprehensive",
                "extract_rules": True,
                "generate_summary": True
            }
        )
        
        return {
            "status": "processing",
            "document_id": str(document.document_id),
            "n8n_workflow_id": n8n_response.get("workflow_id"),
            "message": "Document analysis in progress",
            "estimated_time_seconds": 120
        }
        
    except Exception as e:
        logger.error("Policy document analysis failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/payer/{payer_id}/policies")
async def get_payer_policies(payer_id: str):
    """
    Get all policies for a specific payer
    """
    try:
        # Trigger n8n workflow to fetch payer policies
        n8n_response = await n8n_client.trigger_workflow(
            workflow_name="fetch_payer_policies",
            data={"payer_id": payer_id}
        )
        
        return n8n_response.get("data", {})
        
    except Exception as e:
        logger.error("Failed to fetch payer policies", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


async def parse_policy_interpretation(n8n_response: Dict[str, Any]) -> Dict[str, Any]:
    """Parse n8n response for policy interpretation"""
    data = n8n_response.get("data", {})
    
    return {
        "summary": data.get("summary", ""),
        "coverage_rules": data.get("coverage_rules", []),
        "exclusions": data.get("exclusions", []),
        "limitations": data.get("limitations", []),
        "prior_auth": data.get("prior_authorization_required", []),
        "confidence": data.get("confidence_score", 0.85),
        "interpretation_en": data.get("interpretation_en", ""),
        "interpretation_ar": data.get("interpretation_ar", "")
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "POLICYLINC",
        "description": "Payer Policy Interpretation",
        "version": settings.app_version,
        "features": [
            "AI-powered policy interpretation",
            "Real-time coverage checks",
            "Prior authorization detection",
            "Policy document analysis",
            "Bilingual support",
            "n8n automation integration"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.agents.policylinc_port,
        reload=settings.debug
    )
