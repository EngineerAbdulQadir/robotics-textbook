"""Unit tests for selection endpoint."""

import pytest
from unittest.mock import AsyncMock
from uuid import uuid4

from src.models.schemas import SelectionRequest


@pytest.mark.asyncio
async def test_selection_endpoint_success(client, mock_services):
    """Test successful selection endpoint response."""
    session_id = uuid4()
    selected_text = "Robots are autonomous machines that perform tasks."
    question = "What are the key characteristics?"
    chapter = "Chapter 1"

    # Mock service responses
    mock_services["session"].is_session_valid = AsyncMock(return_value=True)
    mock_services["embedding"].embed_text = AsyncMock(
        return_value=[0.1] * 384
    )
    mock_services["qdrant"].search = AsyncMock(
        return_value=[
            {
                "id": "1",
                "score": 0.88,
                "chapter": "Chapter 1",
                "section": "Basics",
                "content": "Robots have mechanical and electronic components.",
            }
        ]
    )
    mock_services["gemini"].generate_answer = AsyncMock(
        return_value="Key characteristics include autonomy and task execution."
    )

    response = await client.post(
        "/api/v1/chat/selection",
        json={
            "selected_text": selected_text,
            "question": question,
            "session_id": str(session_id),
            "chapter": chapter,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert len(data["sources"]) > 0
    assert data["session_id"] == str(session_id)


@pytest.mark.asyncio
async def test_selection_endpoint_invalid_session(client, mock_services):
    """Test selection endpoint with invalid session."""
    mock_services["session"].is_session_valid = AsyncMock(return_value=False)

    response = await client.post(
        "/api/v1/chat/selection",
        json={
            "selected_text": "Some text here",
            "question": "What is this?",
            "session_id": str(uuid4()),
            "chapter": "Chapter 1",
        },
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_selection_endpoint_too_short(client):
    """Test selection endpoint with text too short."""
    response = await client.post(
        "/api/v1/chat/selection",
        json={
            "selected_text": "Short",  # Less than 5 chars
            "question": "What?",
            "session_id": str(uuid4()),
            "chapter": "Ch1",
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_selection_endpoint_too_long(client):
    """Test selection endpoint with text too long."""
    response = await client.post(
        "/api/v1/chat/selection",
        json={
            "selected_text": "x" * 5001,  # More than 5000 chars
            "question": "What?",
            "session_id": str(uuid4()),
            "chapter": "Ch1",
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_selection_endpoint_question_required(client):
    """Test selection endpoint with missing question."""
    response = await client.post(
        "/api/v1/chat/selection",
        json={
            "selected_text": "Some text here",
            "session_id": str(uuid4()),
            "chapter": "Chapter 1",
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_selection_endpoint_chapter_required(client):
    """Test selection endpoint with missing chapter."""
    response = await client.post(
        "/api/v1/chat/selection",
        json={
            "selected_text": "Some text here",
            "question": "What?",
            "session_id": str(uuid4()),
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_selection_endpoint_response_structure(client, mock_services):
    """Test selection response has correct structure."""
    session_id = uuid4()

    mock_services["session"].is_session_valid = AsyncMock(return_value=True)
    mock_services["embedding"].embed_text = AsyncMock(
        return_value=[0.1] * 384
    )
    mock_services["qdrant"].search = AsyncMock(
        return_value=[
            {
                "id": "1",
                "score": 0.9,
                "chapter": "Chapter 1",
                "section": "Section 1",
                "content": "Content here",
            }
        ]
    )
    mock_services["gemini"].generate_answer = AsyncMock(
        return_value="Answer about selection"
    )

    response = await client.post(
        "/api/v1/chat/selection",
        json={
            "selected_text": "Selected passage about robots",
            "question": "Explain this?",
            "session_id": str(session_id),
            "chapter": "Chapter 1",
        },
    )

    assert response.status_code == 200
    data = response.json()

    # Verify QueryResponse schema
    assert "answer" in data
    assert "sources" in data
    assert "session_id" in data
    assert "message_id" in data
    assert "confidence" in data

    # Verify citation structure
    for source in data["sources"]:
        assert "id" in source
        assert "chapter" in source
        assert "section" in source
        assert "content_excerpt" in source
        assert "confidence_score" in source


@pytest.mark.asyncio
async def test_selection_endpoint_primary_citation_high_confidence(client, mock_services):
    """Test that selected text has highest confidence in citations."""
    session_id = uuid4()

    mock_services["session"].is_session_valid = AsyncMock(return_value=True)
    mock_services["embedding"].embed_text = AsyncMock(
        return_value=[0.1] * 384
    )
    mock_services["qdrant"].search = AsyncMock(
        return_value=[
            {
                "id": "1",
                "score": 0.7,
                "chapter": "Chapter 2",
                "section": "Related",
                "content": "Related content",
            }
        ]
    )
    mock_services["gemini"].generate_answer = AsyncMock(
        return_value="Answer"
    )

    response = await client.post(
        "/api/v1/chat/selection",
        json={
            "selected_text": "Selected text about topic",
            "question": "Explain this?",
            "session_id": str(session_id),
            "chapter": "Chapter 1",
        },
    )

    assert response.status_code == 200
    data = response.json()

    # First source (selected text) should have highest confidence
    # Primary citation has confidence 1.0, but overall is weighted
    assert len(data["sources"]) >= 1
    assert data["sources"][0]["confidence_score"] == 1.0


@pytest.mark.asyncio
async def test_selection_endpoint_service_error(client, mock_services):
    """Test selection endpoint handling service errors."""
    session_id = uuid4()

    mock_services["session"].is_session_valid = AsyncMock(return_value=True)
    mock_services["embedding"].embed_text = AsyncMock(
        side_effect=Exception("Embedding service error")
    )

    response = await client.post(
        "/api/v1/chat/selection",
        json={
            "selected_text": "Some text here",
            "question": "What?",
            "session_id": str(session_id),
            "chapter": "Chapter 1",
        },
    )

    assert response.status_code == 500
