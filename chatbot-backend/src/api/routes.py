"""FastAPI routes for chatbot API - Simplified version without database."""

import logging
from uuid import uuid4
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..config import settings
from ..services.qdrant_service import QdrantService
from ..services.openai_service import OpenAIService
from ..services.cache_service import CacheService
from ..services.rag_service import RAGService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/chat", tags=["Chat"])


class QueryRequest(BaseModel):
    """Request model for chat query."""
    question: str
    session_id: str
    page_context: Optional[str] = None


class SelectionRequest(BaseModel):
    """Request model for selection-based query."""
    question: str
    session_id: str
    selected_text: str
    chapter: str = ""
    section: str = ""


class CitationSchema(BaseModel):
    """Citation/source schema."""
    id: str
    chapter: str = ""
    section: str = ""
    content_excerpt: str = ""
    link: Optional[str] = None
    confidence_score: float = 0.0


class QueryResponse(BaseModel):
    """Response model for chat query."""
    answer: str
    sources: List[CitationSchema] = []
    session_id: str
    message_id: str
    confidence: float = 0.0


@router.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest) -> QueryResponse:
    """
    Process natural language question about textbook content.
    Simplified version - no database, just RAG pipeline.
    """
    cache_service = None
    try:
        logger.info(f"📝 Processing query: {request.question[:50]}...")

        # Initialize services
        cache_service = CacheService(redis_url=settings.redis_url)
        await cache_service.initialize()

        openai_service = OpenAIService(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            embedding_model=settings.openai_embedding_model,
            cache_service=cache_service
        )
        
        qdrant_service = QdrantService(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            collection_name=settings.qdrant_collection_name
        )

        # Process through RAG pipeline
        rag_service = RAGService(openai_service, qdrant_service, cache_service)
        rag_result = await rag_service.process_query(
            question=request.question,
            session_id=request.session_id,
            page_context=request.page_context
        )

        answer = rag_result.get("answer", "Sorry, I couldn't find an answer.")
        confidence = rag_result.get("confidence", 0.0)
        
        # Format citations
        citations = []
        for src in rag_result.get("sources", []):
            payload = src.get("payload", {})
            citations.append(CitationSchema(
                id=str(src.get("id", uuid4())),
                chapter=payload.get("chapter", ""),
                section=payload.get("section", ""),
                content_excerpt=payload.get("content", "")[:300],
                confidence_score=src.get("score", 0.0)
            ))

        message_id = str(uuid4())
        
        logger.info(f"✅ Query complete: {len(citations)} sources, confidence {confidence:.2f}")
        
        return QueryResponse(
            answer=answer,
            sources=citations,
            session_id=request.session_id,
            message_id=message_id,
            confidence=confidence
        )

    except Exception as e:
        logger.error(f"❌ Error processing query: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if cache_service:
            try:
                await cache_service.close()
            except Exception:
                pass


@router.post("/selection", response_model=QueryResponse)
async def selection_endpoint(request: SelectionRequest) -> QueryResponse:
    """Process question about selected text from the textbook."""
    cache_service = None
    try:
        logger.info(f"📖 Processing selection question: {request.question[:50]}...")
        logger.info(f"   Selected text: {request.selected_text[:100]}...")

        # Initialize services
        cache_service = CacheService(redis_url=settings.redis_url)
        await cache_service.initialize()

        openai_service = OpenAIService(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            embedding_model=settings.openai_embedding_model,
            cache_service=cache_service
        )

        # Build a combined question that includes the selected text
        combined_question = f"""The user selected this text from the textbook:
"{request.selected_text}"

Their question about this selection: {request.question}

Please explain or answer based on the selected text."""

        # Use OpenAI directly for selection questions (no RAG needed since we have the context)
        system_prompt = """You are a helpful assistant for a Physical AI and Robotics textbook about ROS 2.
The user has selected some text from the textbook and wants to understand it better.
Explain the selected text clearly and answer their question about it."""

        messages = [{"role": "user", "content": combined_question}]
        
        logger.info(f"🤖 Calling OpenAI for selection answer...")
        answer = await openai_service.chat_completion(messages=messages, system_prompt=system_prompt)
        logger.info(f"✅ Got answer: {answer[:100]}...")

        message_id = str(uuid4())
        
        # Create a citation from the selected text
        citations = [CitationSchema(
            id=str(uuid4()),
            chapter=request.chapter,
            section=request.section,
            content_excerpt=request.selected_text[:300],
            confidence_score=1.0
        )]
        
        return QueryResponse(
            answer=answer,
            sources=citations,
            session_id=request.session_id,
            message_id=message_id,
            confidence=1.0
        )

    except Exception as e:
        logger.error(f"❌ Error processing selection: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if cache_service:
            try:
                await cache_service.close()
            except Exception:
                pass
