"""Integration tests for selection service."""

import pytest
from unittest.mock import AsyncMock
from uuid import uuid4
from datetime import datetime, timedelta

from src.services.selection_service import SelectionService, get_selection_service
from src.models.citation import Citation


@pytest.mark.asyncio
async def test_selection_service_process_success(mock_services):
    """Test selection service with successful processing."""
    service = SelectionService()

    # Mock service responses
    service.embedding_service.embed_text = AsyncMock(
        return_value=[0.1] * 384
    )
    service.qdrant_service.search = AsyncMock(
        return_value=[
            {
                "id": "1",
                "score": 0.85,
                "chapter": "Chapter 1",
                "section": "Intro",
                "content": "Related content about robots",
            }
        ]
    )
    service.gemini_service.generate_answer = AsyncMock(
        return_value="Robots are autonomous machines with mechanical and software components."
    )

    answer, citations, confidence = await service.process_selection_question(
        selected_text="Robots perform tasks autonomously.",
        question="What are robots?",
        chapter="Chapter 1",
        section="Basics",
    )

    assert "Robots" in answer
    assert len(citations) > 0
    assert confidence > 0
    assert citations[0].confidence_score == 1.0  # Selected text has confidence 1.0


@pytest.mark.asyncio
async def test_selection_service_no_related_results(mock_services):
    """Test selection service with no related results."""
    service = SelectionService()

    service.embedding_service.embed_text = AsyncMock(
        return_value=[0.1] * 384
    )
    service.qdrant_service.search = AsyncMock(return_value=[])
    service.gemini_service.generate_answer = AsyncMock(
        return_value="Based on your selection: answer here"
    )

    answer, citations, confidence = await service.process_selection_question(
        selected_text="Specific robotics definition",
        question="What does this mean?",
        chapter="Chapter 2",
    )

    assert len(citations) == 1  # Only the selected text
    assert citations[0].content_excerpt == "Specific robotics definition"


@pytest.mark.asyncio
async def test_selection_service_context_building(mock_services):
    """Test selection context building."""
    service = SelectionService()

    selected = "Robots are autonomous systems"
    related = [
        {
            "chapter": "Chapter 1",
            "section": "Intro",
            "content": "Autonomous systems are self-operating",
        },
        {
            "chapter": "Chapter 2",
            "section": "Advanced",
            "content": "Advanced robotics uses AI",
        },
    ]

    context = service._build_selection_context(
        selected,
        related,
        "Chapter 1",
        "Basics",
    )

    assert "SELECTED TEXT" in context
    assert "Robots are autonomous" in context
    assert "Autonomous systems are self-operating" in context
    assert "Advanced robotics uses AI" in context
    assert "RELATED PASSAGES" in context


@pytest.mark.asyncio
async def test_selection_service_citation_creation(mock_services):
    """Test citation creation with primary + secondary."""
    service = SelectionService()

    selected_text = "Selected passage about AI"
    related_results = [
        {
            "chapter": "Chapter 2",
            "section": "AI Basics",
            "content": "AI is intelligence in machines",
            "score": 0.8,
        }
    ]

    citations = service._create_selection_citations(
        selected_text=selected_text,
        chapter="Chapter 1",
        section="Intro",
        related_results=related_results,
    )

    assert len(citations) == 2
    # Primary citation (selected text)
    assert citations[0].content_excerpt == selected_text
    assert citations[0].confidence_score == 1.0
    # Secondary citation
    assert citations[1].chapter == "Chapter 2"
    assert citations[1].confidence_score == 0.8


@pytest.mark.asyncio
async def test_selection_service_confidence_calculation():
    """Test confidence calculation with weighted primary."""
    service = SelectionService()

    citations = [
        Citation(
            id=uuid4(),
            chapter="Chapter 1",
            section="Intro",
            content_excerpt="Selected text",
            confidence_score=1.0,  # Primary
            expires_at=datetime.utcnow() + timedelta(days=30),
        ),
        Citation(
            id=uuid4(),
            chapter="Chapter 2",
            section="Related",
            content_excerpt="Related content",
            confidence_score=0.7,  # Secondary
            expires_at=datetime.utcnow() + timedelta(days=30),
        ),
    ]

    confidence = service._calculate_confidence(citations)

    # 60% of primary (1.0) + 40% of secondary (0.7) = 0.88
    assert confidence == pytest.approx(0.88)


@pytest.mark.asyncio
async def test_selection_service_context_extraction(mock_services):
    """Test context extraction from selection."""
    service = SelectionService()

    selected = "The robotic arm is a sophisticated mechanical device"
    context = await service.extract_selection_context(selected)

    assert context["text_length"] == len(selected)
    assert context["word_count"] == 10
    assert "robotic" in context["key_terms"]


@pytest.mark.asyncio
async def test_selection_service_same_chapter_filtering(mock_services):
    """Test filtering results to same chapter."""
    service = SelectionService()

    service.embedding_service.embed_text = AsyncMock(
        return_value=[0.1] * 384
    )

    # Return results from different chapters
    service.qdrant_service.search = AsyncMock(
        return_value=[
            {
                "id": "1",
                "score": 0.9,
                "chapter": "Chapter 1",  # Same
                "section": "Basics",
                "content": "Chapter 1 content",
            },
            {
                "id": "2",
                "score": 0.8,
                "chapter": "Chapter 2",  # Different
                "section": "Advanced",
                "content": "Chapter 2 content",
            },
            {
                "id": "3",
                "score": 0.75,
                "chapter": "Chapter 1",  # Same
                "section": "Details",
                "content": "More chapter 1",
            },
        ]
    )
    service.gemini_service.generate_answer = AsyncMock(
        return_value="Answer"
    )

    answer, citations, confidence = await service.process_selection_question(
        selected_text="Selection from Chapter 1",
        question="Question?",
        chapter="Chapter 1",
    )

    # Should have primary citation (selected) + 2 from Chapter 1
    assert len(citations) <= 3


@pytest.mark.asyncio
async def test_selection_service_singleton():
    """Test selection service singleton pattern."""
    service1 = get_selection_service()
    service2 = get_selection_service()

    assert service1 is service2


@pytest.mark.asyncio
async def test_selection_service_empty_citation_confidence():
    """Test confidence with no citations."""
    service = SelectionService()

    confidence = service._calculate_confidence([])

    assert confidence == 0.0


@pytest.mark.asyncio
async def test_selection_service_single_citation_confidence():
    """Test confidence with only primary citation."""
    service = SelectionService()

    citations = [
        Citation(
            id=uuid4(),
            chapter="Chapter 1",
            section="Intro",
            content_excerpt="Selected",
            confidence_score=1.0,
            expires_at=datetime.utcnow() + timedelta(days=30),
        )
    ]

    confidence = service._calculate_confidence(citations)

    assert confidence == 1.0
