"""
CLAIMLINC - Claims Rejection Analysis
AI-powered claims rejection analysis and resolution
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from shared.config.settings import settings
from shared.models.base import HealthCheckResponse
from shared.models.claims import (
    ClaimAnalysisRequest,
    ClaimAnalysis,
    ClaimResubmissionRequest
)
from shared.utils.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management"""
    logger.info("Starting CLAIMLINC")
    yield
    logger.info("Shutting down CLAIMLINC")


app = FastAPI(
    title="CLAIMLINC - Claims Analysis",
    description="AI-powered claims rejection analysis and resolution",
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


@app.post("/api/v1/analyze", response_model=ClaimAnalysis)
async def analyze_claim(request: ClaimAnalysisRequest):
    """
    Analyze rejected claim and suggest corrections
    Uses GPT-4 for intelligent analysis
    """
    try:
        logger.info(
            "Analyzing claim",
            claim_id=str(request.claim.id),
            payer=request.claim.payer_id
        )
        
        # TODO: Implement actual AI analysis with OpenAI
        # For now, return mock response
        analysis = ClaimAnalysis(
            claim_id=request.claim.id,
            confidence_score=0.85,
            automation_available=False,
            manual_review_required=True,
            root_causes=["Incorrect diagnosis code", "Missing authorization"],
            recommendations_en=["Update ICD-10 code", "Obtain prior authorization"],
            recommendations_ar=["تحديث رمز ICD-10", "الحصول على تفويض مسبق"],
            next_actions=["Review coding", "Contact payer"],
            ai_model_used=settings.openai.model_gpt4
        )
        
        return analysis
        
    except Exception as e:
        logger.error("Claim analysis failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/resubmit")
async def resubmit_claim(request: ClaimResubmissionRequest):
    """
    Resubmit corrected claim to NPHIES
    """
    try:
        logger.info(
            "Resubmitting claim",
            original_claim_id=str(request.original_claim_id),
            is_appeal=request.is_appeal
        )
        
        # TODO: Implement NPHIES resubmission
        return {
            "status": "submitted",
            "claim_id": str(request.corrected_claim.id),
            "nphies_claim_id": "NPH-12345",
            "message": "Claim resubmitted successfully"
        }
        
    except Exception as e:
        logger.error("Claim resubmission failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "CLAIMLINC",
        "description": "Claims Rejection Analysis",
        "version": settings.app_version,
        "features": [
            "AI-powered analysis",
            "Automated corrections",
            "NPHIES integration",
            "Bilingual support"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.agents.claimlinc_port,
        reload=settings.debug
    )
