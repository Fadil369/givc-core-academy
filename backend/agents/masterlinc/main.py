"""
MASTERLINC - Central Orchestration Hub
Routes requests to specialized agents based on context
"""

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time
from typing import Dict, Any
from uuid import uuid4

from shared.config.settings import settings
from shared.models.base import (
    OrchestrationContext, 
    HealthCheckResponse, 
    ErrorResponse,
    AgentType
)
from shared.utils.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management"""
    logger.info("Starting MASTERLINC orchestration hub")
    yield
    logger.info("Shutting down MASTERLINC")


app = FastAPI(
    title="MASTERLINC - BrainSAIT Orchestration Hub",
    description="Central coordination system for all BrainSAIT LINC agents",
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs" if settings.api_docs_enabled else None,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_credentials,
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time header"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    return HealthCheckResponse(
        status="healthy",
        version=settings.app_version,
        environment=settings.environment,
        database=True,  # TODO: Implement actual checks
        redis=True,
        external_apis={
            "openai": True,
            "nphies": True,
        }
    )


@app.post("/api/v1/orchestrate")
async def orchestrate_request(request: Dict[str, Any]):
    """
    Main orchestration endpoint
    Routes requests to appropriate agents
    """
    request_id = str(uuid4())
    
    try:
        # Determine agent type
        agent_type = AgentType(request.get("agent_type", "HEALTHCARELINC"))
        
        # Create orchestration context
        context = OrchestrationContext(
            request_id=request_id,
            agent_type=agent_type,
            source=request.get("source", "api"),
            priority=request.get("priority", "normal"),
        )
        
        logger.info(
            "Orchestrating request",
            request_id=request_id,
            agent_type=agent_type.value
        )
        
        # Route to appropriate agent
        result = await route_to_agent(context, request)
        
        return {
            "request_id": request_id,
            "status": "success",
            "agent": agent_type.value,
            "result": result
        }
        
    except Exception as e:
        logger.error("Orchestration failed", error=str(e), request_id=request_id)
        raise HTTPException(status_code=500, detail=str(e))


async def route_to_agent(context: OrchestrationContext, request: Dict[str, Any]) -> Dict[str, Any]:
    """Route request to appropriate agent"""
    
    agent_urls = {
        AgentType.HEALTHCARELINC: settings.get_agent_base_url("healthcarelinc"),
        AgentType.CLAIMLINC: settings.get_agent_base_url("claimlinc"),
        AgentType.TTLINC: settings.get_agent_base_url("ttlinc"),
    }
    
    # For now, return a mock response
    # TODO: Implement actual HTTP calls to agents
    return {
        "message": f"Routed to {context.agent_type.value}",
        "context": context.dict()
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "MASTERLINC",
        "description": "BrainSAIT Central Orchestration Hub",
        "version": settings.app_version,
        "agents_managed": [agent.value for agent in AgentType],
        "docs": "/docs" if settings.api_docs_enabled else None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.agents.masterlinc_port,
        reload=settings.debug
    )
