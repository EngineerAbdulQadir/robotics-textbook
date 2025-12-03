"""Unit tests for chat query endpoint."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from uuid import uuid4
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.testclient import TestClient

from src.main import app
from src.models.schemas import QueryRequest, QueryResponse
from src.config import settings


@pytest.mark.asyncio
async def test_query_endpoint_success(client, mock_services):
    """Test successful query endpoint response."""
    # Prepare test data
    session_id = uuid4()
    question = "What is robotics?"
    page_context = "Chapter 1"

    # Mock service responses
    mock_services["session"].is_session_valid = AsyncMock(return_value=True)
    mock_services["embedding"].embed_text = AsyncMock(
        return_value=[0.1] * 384  # Mock 384-dim embedding
    )
    mock_services["qdrant"].search = AsyncMock(
        return_value=[
            {
                "id": "1",
                "score": 0.9,
                "chapter": "Chapter 1",
                "section": "Introduction",
                "content": "Robotics is the study of robots...",
            }
        ]
    )
    mock_services["gemini"].generate_answer = AsyncMock(
        return_value="Robotics is the study and design of robots."
    )

    # Make request
    response = await client.post(
        "/api/v1/chat/query",
        json={
            "question": question,
            "session_id": str(session_id),
            "page_context": page_context,
        },
    )

    # Assert response
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "Robotics is the study and design of robots."
    assert len(data["sources"]) > 0
    assert data["session_id"] == str(session_id)
    assert "message_id" in data
    assert 0 <= data["confidence"] <= 1


@pytest.mark.asyncio
async def test_query_endpoint_invalid_session(client, mock_services):
    """Test query endpoint with invalid session."""
    # Mock invalid session
    mock_services["session"].is_session_valid = AsyncMock(return_value=False)

    response = await client.post(
        "/api/v1/chat/query",
        json={
            "question": "What is robotics?",
            "session_id": str(uuid4()),
        },
    )

    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_query_endpoint_empty_results(client, mock_services):
    """Test query endpoint when no relevant content found."""
    session_id = uuid4()

    # Mock empty search results
    mock_services["session"].is_session_valid = AsyncMock(return_value=True)
    mock_services["embedding"].embed_text = AsyncMock(
        return_value=[0.1] * 384
    )
    mock_services["qdrant"].search = AsyncMock(return_value=[])

    response = await client.post(
        "/api/v1/chat/query",
        json={
            "question": "Unknown obscure topic?",
            "session_id": str(session_id),
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "don't find" in data["answer"].lower()
    assert len(data["sources"]) == 0
    assert data["confidence"] == 0.0


@pytest.mark.asyncio
async def test_query_endpoint_validation_error(client):
    """Test query endpoint with invalid input."""
    response = await client.post(
        "/api/v1/chat/query",
        json={
            "question": "",  # Empty question
            "session_id": str(uuid4()),
        },
    )

    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_query_endpoint_rate_limit_graceful_degradation(
    client, mock_services
):
    """Test graceful degradation under rate limit."""
    session_id = uuid4()

    # Mock rate limit exception from Gemini
    mock_services["session"].is_session_valid = AsyncMock(return_value=True)
    mock_services["embedding"].embed_text = AsyncMock(
        return_value=[0.1] * 384
    )
    mock_services["qdrant"].search = AsyncMock(
        return_value=[
            {
                "id": "1",
                "score": 0.9,
                "chapter": "Ch1",
                "section": "Intro",
                "content": "Content",
            }
        ]
    )

    # Simulate rate limit
    from src.utils.errors import RateLimitException
    mock_services["gemini"].generate_answer = AsyncMock(
        side_effect=RateLimitException("Rate limited")
    )

    response = await client.post(
        "/api/v1/chat/query",
        json={
            "question": "What is AI?",
            "session_id": str(session_id),
        },
    )

    if settings.enable_rate_limit_graceful_degradation:
        assert response.status_code == 429
    else:
        assert response.status_code == 429


@pytest.mark.asyncio
async def test_query_endpoint_question_length_validation(client):
    """Test question length validation."""
    # Test too long question (max 500 chars)
    long_question = "x" * 501

    response = await client.post(
        "/api/v1/chat/query",
        json={
            "question": long_question,
            "session_id": str(uuid4()),
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_query_endpoint_response_structure(client, mock_services):
    """Test that response has correct structure."""
    session_id = uuid4()

    # Setup mocks
    mock_services["session"].is_session_valid = AsyncMock(return_value=True)
    mock_services["embedding"].embed_text = AsyncMock(
        return_value=[0.1] * 384
    )
    mock_services["qdrant"].search = AsyncMock(
        return_value=[
            {
                "id": "1",
                "score": 0.95,
                "chapter": "Chapter 1",
                "section": "Basics",
                "content": "Answer content here",
            }
        ]
    )
    mock_services["gemini"].generate_answer = AsyncMock(
        return_value="Test answer"
    )

    response = await client.post(
        "/api/v1/chat/query",
        json={
            "question": "Test?",
            "session_id": str(session_id),
        },
    )

    data = response.json()

    # Verify response structure matches QueryResponse schema
    assert "answer" in data
    assert "sources" in data
    assert "session_id" in data
    assert "message_id" in data
    assert "confidence" in data

    # Verify sources structure
    for source in data["sources"]:
        assert "id" in source
        assert "chapter" in source
        assert "section" in source
        assert "content_excerpt" in source
        assert "confidence_score" in source
