"""
TTLINC - Medical Translation Service
Bidirectional Arabic-English medical translation
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from shared.config.settings import settings
from shared.models.base import HealthCheckResponse
from shared.models.translation import (
    TranslationRequest,
    TranslationResponse,
    QualityMetrics,
    TranslationStatus
)
from shared.utils.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management"""
    logger.info("Starting TTLINC")
    yield
    logger.info("Shutting down TTLINC")


app = FastAPI(
    title="TTLINC - Medical Translation",
    description="Bidirectional Arabic-English medical translation",
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


@app.post("/api/v1/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    """
    Translate medical text between Arabic and English
    Uses GPT-4-Turbo for high-quality translation
    """
    try:
        logger.info(
            "Translating text",
            request_id=str(request.request_id),
            source_lang=request.source_language.value,
            target_lang=request.target_language.value,
            document_type=request.document_type.value
        )
        
        # TODO: Implement actual translation with OpenAI
        # For now, return mock response
        quality_metrics = QualityMetrics(
            completeness_score=0.95,
            terminology_accuracy=0.92,
            formatting_preserved=True,
            context_consistency=0.90,
            medical_accuracy=0.93,
            overall_score=0.92,
            meets_threshold=True,
            threshold_used=request.quality_threshold
        )
        
        response = TranslationResponse(
            request_id=request.request_id,
            status=TranslationStatus.COMPLETED,
            source_text=request.source_text,
            translated_text="[Translated text would appear here]",
            source_language=request.source_language,
            target_language=request.target_language,
            quality_metrics=quality_metrics,
            model_used=settings.openai.model_gpt4_turbo,
            processing_time_ms=1500,
            confidence_score=0.92
        )
        
        return response
        
    except Exception as e:
        logger.error("Translation failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "TTLINC",
        "description": "Medical Translation Service",
        "version": settings.app_version,
        "languages": ["Arabic", "English"],
        "document_types": [
            "clinical_note",
            "discharge_summary",
            "lab_report",
            "prescription"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.agents.ttlinc_port,
        reload=settings.debug
    )
