"""FastAPI application entry point."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import logging

from .config import settings
from .models.schemas import HealthCheckResponse
from .db import get_engine
from .services.qdrant_service import QdrantService
from .services.openai_service import OpenAIService
from .services.cache_service import CacheService
from .middleware.rate_limit import RateLimitMiddleware
from .api.routes import router as chat_router
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

# Configure logging
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)


# Create FastAPI app
app = FastAPI(
    title="RAG Chatbot API",
    description="Retrieval-Augmented Generation chatbot for Physical AI Textbook",
    version="0.1.0",
)

# Add CORS middleware FIRST (must be before rate limiting to handle preflight requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting middleware (after CORS so preflight requests get CORS headers)
if settings.rate_limit_enabled:
    app.add_middleware(RateLimitMiddleware)

# Include routers
app.include_router(chat_router)


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("🚀 Starting RAG Chatbot API...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug: {settings.debug}")
    logger.info(f"CORS Allowed Origins: {settings.allowed_origins}")
    logger.info(f"Allowed Origins Type: {type(settings.allowed_origins)}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("🛑 Shutting down RAG Chatbot API...")


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint."""
    return {"message": "RAG Chatbot API", "version": "0.1.0"}


@app.get("/api/v1/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check():
    """Health check endpoint."""
    # Check Qdrant
    qdrant_service = QdrantService(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
        collection_name=settings.qdrant_collection_name
    )
    qdrant_ok = await qdrant_service.health_check()

    # Check OpenAI (basic check - API key configured)
    openai_ok = bool(settings.openai_api_key)

    # Check Cache/Redis
    cache_service = CacheService(redis_url=settings.redis_url)
    await cache_service.initialize()
    cache_ok = await cache_service.health_check()

    # Determine overall status
    if qdrant_ok and openai_ok and cache_ok:
        status = "ok"
    elif (qdrant_ok + openai_ok + cache_ok) >= 2:
        status = "degraded"
    else:
        status = "down"

    return HealthCheckResponse(
        status=status,
        version="0.1.0",
        qdrant_status="healthy" if qdrant_ok else "down",
        neon_status="healthy",  # PostgreSQL status would be checked here in production
        gemini_status="healthy" if openai_ok else "down",  # Changed to OpenAI status (field name kept for compatibility)
    )


@app.get("/api/v1/docs", tags=["Documentation"])
async def get_docs():
    """Get API documentation."""
    return {
        "title": "RAG Chatbot API Documentation",
        "version": "0.1.0",
        "endpoints": {
            "POST /api/v1/chat/query": "Send question about textbook content",
            "POST /api/v1/chat/selection": "Ask question about selected text",
            "GET /api/v1/chat/history": "Retrieve conversation history",
            "GET /api/v1/health": "Service health status",
            "GET /metrics": "Prometheus metrics",
        },
    }


@app.get("/metrics", tags=["Monitoring"])
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
