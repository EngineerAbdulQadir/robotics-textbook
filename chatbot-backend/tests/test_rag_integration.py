"""Integration tests for RAG pipeline."""

import pytest
from uuid import uuid4
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.rag_service import RAGService, get_rag_service
from src.models.citation import Citation
from src.config import settings


@pytest.mark.asyncio
async def test_rag_service_process_query_with_results(mock_db_session, mock_services):
    """Test RAG service with search results."""
    rag_service = RAGService()

    # Mock the underlying services
    rag_service.embedding_service.embed_text = mock_services["embedding"].embed_text
    rag_service.qdrant_service.search = mock_services["qdrant"].search
    rag_service.gemini_service.generate_answer = mock_services["gemini"].generate_answer

    # Mock service responses
    mock_services["embedding"].embed_text = AsyncMock(
        return_value=[0.1] * 384
    )
    mock_services["qdrant"].search = AsyncMock(
        return_value=[
            {
                "id": "1",
                "score": 0.95,
                "chapter": "Chapter 1",
                "section": "Fundamentals",
                "content": "Robotics combines mechanical and software engineering.",
            },
            {
                "id": "2",
                "score": 0.88,
                "chapter": "Chapter 2",
                "section": "Applications",
                "content": "Robots are used in manufacturing and medicine.",
            },
        ]
    )
    mock_services["gemini"].generate_answer = AsyncMock(
        return_value="Robotics is the integration of mechanical and software engineering."
    )

    # Process query
    answer, citations, confidence = await rag_service.process_query(
        question="What is robotics?"
    )

    # Assertions
    assert answer == "Robotics is the integration of mechanical and software engineering."
    assert len(citations) == 2
    assert 0 <= confidence <= 1
    assert confidence > 0.8  # High confidence with 2 good results


@pytest.mark.asyncio
async def test_rag_service_process_query_no_results(mock_services):
    """Test RAG service when no results found."""
    rag_service = RAGService()

    # Mock empty results
    mock_services["embedding"].embed_text = AsyncMock(
        return_value=[0.1] * 384
    )
    mock_services["qdrant"].search = AsyncMock(return_value=[])

    answer, citations, confidence = await rag_service.process_query(
        question="Unknown obscure topic?"
    )

    assert "don't find" in answer.lower()
    assert len(citations) == 0
    assert confidence == 0.0


@pytest.mark.asyncio
async def test_rag_service_build_context(mock_services):
    """Test context building from search results."""
    rag_service = RAGService()

    search_results = [
        {
            "chapter": "Chapter 1",
            "section": "Introduction",
            "content": "This is about basics.",
        },
        {
            "chapter": "Chapter 2",
            "section": "Advanced",
            "content": "This is about advanced topics.",
        },
    ]

    context = rag_service._build_context(search_results)

    assert "Chapter 1" in context
    assert "Chapter 2" in context
    assert "Introduction" in context
    assert "Advanced" in context
    assert "basics" in context
    assert "advanced" in context


@pytest.mark.asyncio
async def test_rag_service_create_citations(mock_services):
    """Test citation creation from search results."""
    rag_service = RAGService()

    search_results = [
        {
            "chapter": "Chapter 1",
            "section": "Basics",
            "content": "Content about basics",
            "score": 0.95,
        },
        {
            "chapter": "Chapter 2",
            "section": "Advanced",
            "content": "Content about advanced topics",
            "score": 0.85,
        },
    ]

    citations = rag_service._create_citations(search_results)

    assert len(citations) == 2
    assert citations[0].chapter == "Chapter 1"
    assert citations[0].section == "Basics"
    assert citations[0].confidence_score == 0.95
    assert citations[1].chapter == "Chapter 2"
    assert citations[1].confidence_score == 0.85


@pytest.mark.asyncio
async def test_rag_service_calculate_confidence():
    """Test confidence score calculation."""
    rag_service = RAGService()

    # Create mock citations
    citations = [
        Citation(
            id=uuid4(),
            chapter="Ch1",
            section="Sec1",
            content_excerpt="Content",
            confidence_score=0.95,
            expires_at=datetime.utcnow() + timedelta(days=30),
        ),
        Citation(
            id=uuid4(),
            chapter="Ch2",
            section="Sec2",
            content_excerpt="Content",
            confidence_score=0.85,
            expires_at=datetime.utcnow() + timedelta(days=30),
        ),
    ]

    confidence = rag_service._calculate_confidence(citations)

    assert confidence == pytest.approx(0.9)  # Average of 0.95 and 0.85


@pytest.mark.asyncio
async def test_rag_service_calculate_confidence_empty():
    """Test confidence calculation with empty citations."""
    rag_service = RAGService()

    confidence = rag_service._calculate_confidence([])

    assert confidence == 0.0


@pytest.mark.asyncio
async def test_rag_service_hallucination_detection(mock_services):
    """Test hallucination detection in RAG service."""
    rag_service = RAGService()

    # Test with hallucination phrase
    with pytest.raises(Exception):  # HallucationDetectedException
        await rag_service._check_hallucination(
            answer="I believe this is the answer",
            context="Some context",
        )


@pytest.mark.asyncio
async def test_rag_service_hallucination_clean_answer(mock_services):
    """Test clean answer passes hallucination check."""
    rag_service = RAGService()

    # Should not raise exception
    await rag_service._check_hallucination(
        answer="According to the textbook, the answer is clear.",
        context="Some context",
    )


@pytest.mark.asyncio
async def test_rag_service_global_instance():
    """Test RAG service singleton pattern."""
    service1 = get_rag_service()
    service2 = get_rag_service()

    assert service1 is service2


@pytest.mark.asyncio
async def test_rag_pipeline_end_to_end(mock_services):
    """Test complete RAG pipeline."""
    rag_service = RAGService()

    # Setup mocks
    rag_service.embedding_service.embed_text = AsyncMock(
        return_value=[0.1] * 384
    )
    rag_service.qdrant_service.search = AsyncMock(
        return_value=[
            {
                "id": "1",
                "score": 0.92,
                "chapter": "Chapter 1",
                "section": "Intro",
                "content": "Robotics fundamentals here.",
            }
        ]
    )
    rag_service.gemini_service.generate_answer = AsyncMock(
        return_value="Robotics fundamentals include mechanics and control."
    )

    # Execute pipeline
    answer, citations, confidence = await rag_service.process_query(
        question="What are robotics fundamentals?",
        top_k=5,
        score_threshold=0.5,
    )

    # Verify all steps executed
    assert answer is not None
    assert len(citations) > 0
    assert confidence > 0
    assert rag_service.embedding_service.embed_text.called
    assert rag_service.qdrant_service.search.called
    assert rag_service.gemini_service.generate_answer.called
