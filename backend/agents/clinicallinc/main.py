"""
CLINICALLINC - Clinical Decision Support System
AI-powered clinical decision support, drug interactions, and care pathways
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Dict, Any, List

from shared.config.settings import settings
from shared.models.base import HealthCheckResponse
from shared.models.clinical import (
    ClinicalDecisionRequest,
    ClinicalDecisionResponse,
    DrugInteractionCheck,
    DrugInteractionResponse,
    CarePathwayRequest,
    CarePathwayResponse,
    DiagnosticSuggestion
)
from shared.utils.logger import get_logger
from shared.integrations.n8n_client import N8NClient

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management"""
    logger.info("Starting CLINICALLINC")
    yield
    logger.info("Shutting down CLINICALLINC")


app = FastAPI(
    title="CLINICALLINC - Clinical Decision Support",
    description="AI-powered clinical decision support and care pathways",
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


@app.post("/api/v1/clinical-decision", response_model=ClinicalDecisionResponse)
async def clinical_decision_support(request: ClinicalDecisionRequest):
    """
    Provide clinical decision support based on patient data
    Uses AI to analyze symptoms, labs, and history
    """
    try:
        logger.info(
            "Processing clinical decision request",
            request_id=str(request.request_id),
            patient_id=str(request.patient_id)
        )
        
        # Trigger n8n workflow for clinical decision support
        n8n_response = await n8n_client.trigger_workflow(
            workflow_name="clinical_decision_support",
            data={
                "request_id": str(request.request_id),
                "patient_id": str(request.patient_id),
                "chief_complaint": request.chief_complaint,
                "symptoms": request.symptoms,
                "vital_signs": request.vital_signs,
                "lab_results": request.lab_results,
                "medical_history": request.medical_history,
                "medications": request.current_medications,
                "use_ai": True,
                "model": settings.openai.model_gpt4
            }
        )
        
        # Parse clinical decision response
        decision_data = n8n_response.get("data", {})
        
        return ClinicalDecisionResponse(
            request_id=request.request_id,
            differential_diagnosis=decision_data.get("differential_diagnosis", []),
            recommended_tests=decision_data.get("recommended_tests", []),
            treatment_recommendations=decision_data.get("treatment_recommendations", []),
            red_flags=decision_data.get("red_flags", []),
            urgency_level=decision_data.get("urgency_level", "routine"),
            confidence_score=decision_data.get("confidence_score", 0.8),
            clinical_notes=decision_data.get("clinical_notes", ""),
            evidence_based_guidelines=decision_data.get("guidelines", []),
            ai_model_used=settings.openai.model_gpt4,
            n8n_workflow_id=n8n_response.get("workflow_id")
        )
        
    except Exception as e:
        logger.error("Clinical decision support failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/drug-interactions", response_model=DrugInteractionResponse)
async def check_drug_interactions(request: DrugInteractionCheck):
    """
    Check for drug interactions between medications
    Real-time safety analysis
    """
    try:
        logger.info(
            "Checking drug interactions",
            request_id=str(request.request_id),
            num_medications=len(request.medications)
        )
        
        # Trigger n8n workflow for drug interaction check
        n8n_response = await n8n_client.trigger_workflow(
            workflow_name="drug_interaction_check",
            data={
                "request_id": str(request.request_id),
                "patient_id": str(request.patient_id) if request.patient_id else None,
                "medications": request.medications,
                "check_allergies": True,
                "check_contraindications": True,
                "severity_threshold": "moderate"
            }
        )
        
        # Parse interaction response
        interaction_data = n8n_response.get("data", {})
        
        return DrugInteractionResponse(
            request_id=request.request_id,
            has_interactions=interaction_data.get("has_interactions", False),
            interactions=interaction_data.get("interactions", []),
            severity_summary=interaction_data.get("severity_summary", {}),
            recommendations=interaction_data.get("recommendations", []),
            contraindications=interaction_data.get("contraindications", []),
            warnings=interaction_data.get("warnings", []),
            safe_to_prescribe=interaction_data.get("safe_to_prescribe", True),
            n8n_workflow_id=n8n_response.get("workflow_id")
        )
        
    except Exception as e:
        logger.error("Drug interaction check failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/care-pathway", response_model=CarePathwayResponse)
async def generate_care_pathway(request: CarePathwayRequest):
    """
    Generate evidence-based care pathway for a condition
    Provides step-by-step clinical protocol
    """
    try:
        logger.info(
            "Generating care pathway",
            request_id=str(request.request_id),
            condition=request.condition
        )
        
        # Trigger n8n workflow for care pathway generation
        n8n_response = await n8n_client.trigger_workflow(
            workflow_name="care_pathway_generation",
            data={
                "request_id": str(request.request_id),
                "patient_id": str(request.patient_id),
                "condition": request.condition,
                "severity": request.severity,
                "patient_age": request.patient_age,
                "comorbidities": request.comorbidities,
                "include_medications": True,
                "include_monitoring": True,
                "bilingual": True
            }
        )
        
        # Parse care pathway response
        pathway_data = n8n_response.get("data", {})
        
        return CarePathwayResponse(
            request_id=request.request_id,
            condition=request.condition,
            pathway_steps=pathway_data.get("pathway_steps", []),
            medications=pathway_data.get("medications", []),
            monitoring_parameters=pathway_data.get("monitoring_parameters", []),
            expected_outcomes=pathway_data.get("expected_outcomes", []),
            red_flags=pathway_data.get("red_flags", []),
            follow_up_schedule=pathway_data.get("follow_up_schedule", []),
            evidence_level=pathway_data.get("evidence_level", "moderate"),
            guidelines_reference=pathway_data.get("guidelines_reference", []),
            pathway_en=pathway_data.get("pathway_en", ""),
            pathway_ar=pathway_data.get("pathway_ar", ""),
            n8n_workflow_id=n8n_response.get("workflow_id")
        )
        
    except Exception as e:
        logger.error("Care pathway generation failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/diagnostic-suggestions")
async def get_diagnostic_suggestions(
    symptoms: List[str],
    patient_age: int,
    gender: str,
    vital_signs: Dict[str, Any] = None
) -> List[DiagnosticSuggestion]:
    """
    Get AI-powered diagnostic suggestions based on symptoms
    """
    try:
        # Trigger n8n workflow for diagnostic suggestions
        n8n_response = await n8n_client.trigger_workflow(
            workflow_name="diagnostic_suggestions",
            data={
                "symptoms": symptoms,
                "patient_age": patient_age,
                "gender": gender,
                "vital_signs": vital_signs or {},
                "use_ai": True,
                "model": settings.openai.model_gpt4
            }
        )
        
        suggestions = n8n_response.get("data", {}).get("suggestions", [])
        return [DiagnosticSuggestion(**s) for s in suggestions]
        
    except Exception as e:
        logger.error("Diagnostic suggestions failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "CLINICALLINC",
        "description": "Clinical Decision Support System",
        "version": settings.app_version,
        "features": [
            "AI-powered clinical decision support",
            "Drug interaction checking",
            "Care pathway generation",
            "Diagnostic suggestions",
            "Evidence-based guidelines",
            "Bilingual support",
            "n8n automation integration"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.agents.clinicallinc_port,
        reload=settings.debug
    )
