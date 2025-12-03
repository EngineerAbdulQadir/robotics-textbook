"""Pydantic request/response schemas."""

from typing import List, Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


# Request Schemas
class QueryRequest(BaseModel):
    """Chat query request."""

    question: str = Field(..., min_length=1, max_length=500)
    session_id: UUID
    page_context: Optional[str] = None


class SelectionRequest(BaseModel):
    """Selected text query request."""

    selected_text: str = Field(..., min_length=5, max_length=5000)
    question: str = Field(..., min_length=1, max_length=500)
    session_id: UUID
    chapter: str


# Response Schemas
class CitationSchema(BaseModel):
    """Citation in answer."""

    id: UUID
    chapter: str
    section: str
    content_excerpt: str
    link: Optional[str] = None
    confidence_score: float = 0.0

    class Config:
        from_attributes = True


class MessageSchema(BaseModel):
    """Chat message."""

    id: UUID
    conversation_id: UUID
    role: str
    content: str
    timestamp: datetime
    source_references: List[dict] = []

    class Config:
        from_attributes = True


class ConversationSchema(BaseModel):
    """Conversation with messages."""

    id: UUID
    user_session_id: UUID
    page_context: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    messages: List[MessageSchema] = []

    class Config:
        from_attributes = True


class QueryResponse(BaseModel):
    """Chat query response."""

    answer: str
    sources: List[CitationSchema]
    session_id: UUID
    message_id: UUID
    confidence: Optional[float] = 0.9

    class Config:
        from_attributes = True


class HealthCheckResponse(BaseModel):
    """Health check response."""

    status: str  # ok, degraded, down
    version: str
    qdrant_status: str
    neon_status: str
    gemini_status: str
