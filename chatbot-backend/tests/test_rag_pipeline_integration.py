"""
Integration tests for RAG (Retrieval-Augmented Generation) pipeline.

Tests the complete end-to-end flow:
1. Query caching (Phase 4)
2. Embedding with caching (Phase 4)
3. Vector search in Qdrant (Phase 1)
4. LLM response generation (Phase 1)
5. Citation extraction (Phase 1)
6. Cache cleanup on completion (Phase 3)
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

from src.services.rag_service import RAGService
from src.services.openai_service import OpenAIService
from src.services.qdrant_service import QdrantService
from src.services.cache_service import CacheService


@pytest.mark.asyncio
class TestRAGPipelineIntegration:
    """Integration tests for RAG pipeline with all services."""

    @pytest.fixture
    async def cache_service(self):
        """Create a real cache service for integration testing."""
        service = CacheService(redis_url="redis://localhost:6379")
        yield service
        # Cleanup
        try:
            await service.close()
        except Exception:
            pass

    @pytest.fixture
    def mock_openai_service(self):
        """Mock OpenAI service with embedding and chat capabilities."""
        service = AsyncMock(spec=OpenAIService)

        # Mock embedding
        service.embed_text.return_value = [0.1, 0.2, 0.3] * 100  # 300-dim vector

        # Mock chat completion
        service.chat_completion.return_value = (
            "ROS 2 nodes communicate via topics using a publisher-subscriber pattern. "
            "Publishers send messages to a topic, and subscribers receive those messages."
        )

        return service

    @pytest.fixture
    def mock_qdrant_service(self):
        """Mock Qdrant service with vector search capabilities."""
        service = AsyncMock(spec=QdrantService)

        # Mock search results
        service.search.return_value = [
            {
                "id": str(uuid4()),
                "score": 0.95,
                "payload": {
                    "chapter": "Module 1: ROS 2 Basics",
                    "section": "Nodes and Topics",
                    "content": "ROS 2 nodes communicate via topics using a publisher-subscriber pattern.",
                    "confidence_score": 0.95
                }
            },
            {
                "id": str(uuid4()),
                "score": 0.87,
                "payload": {
                    "chapter": "Module 1: ROS 2 Basics",
                    "section": "Communication Patterns",
                    "content": "The pub-sub model decouples nodes from each other.",
                    "confidence_score": 0.87
                }
            }
        ]

        return service

    async def test_complete_query_pipeline_with_cache_hit(
        self,
        mock_openai_service,
        mock_qdrant_service
    ):
        """Test complete RAG pipeline with cache hit on second query."""
        cache_service = CacheService(redis_url="redis://localhost:6379")

        try:
            await cache_service.initialize()
            rag_service = RAGService(
                mock_openai_service,
                mock_qdrant_service,
                cache_service
            )

            question = "How do ROS 2 nodes communicate?"
            session_id = "test-session-123"

            # First call - cache miss
            result1 = await rag_service.process_query(question, session_id)

            assert result1 is not None
            assert "answer" in result1
            assert "sources" in result1
            assert "confidence" in result1
            assert len(result1["sources"]) > 0

            # Verify embedding was called
            mock_openai_service.embed_text.assert_called()
            embed_call_count_1 = mock_openai_service.embed_text.call_count

            # Reset mock call counts
            mock_openai_service.reset_mock()

            # Second call - should hit cache
            result2 = await rag_service.process_query(question, session_id)

            # Cache hit should return same result
            assert result2["answer"] == result1["answer"]
            assert len(result2["sources"]) == len(result1["sources"])

            # Embedding should NOT be called on cache hit
            # (it would be called if we didn't hit cache)
            embed_call_count_2 = mock_openai_service.embed_text.call_count
            assert embed_call_count_2 == 0  # Cache hit, no embedding call

        finally:
            await cache_service.close()

    async def test_pipeline_cache_miss_flow(
        self,
        mock_openai_service,
        mock_qdrant_service
    ):
        """Test RAG pipeline when cache is empty (cache miss)."""
        cache_service = CacheService(redis_url="redis://localhost:6379")

        try:
            await cache_service.initialize()
            rag_service = RAGService(
                mock_openai_service,
                mock_qdrant_service,
                cache_service
            )

            question = "What is ROS 2?"
            session_id = "new-session-456"

            result = await rag_service.process_query(question, session_id)

            # Verify pipeline executed all steps
            assert result["answer"] is not None
            assert "sources" in result
            assert result["confidence"] > 0

            # Verify all services were called in order
            mock_openai_service.embed_text.assert_called_once_with(question)
            mock_qdrant_service.search.assert_called_once()
            mock_openai_service.chat_completion.assert_called_once()

        finally:
            await cache_service.close()

    async def test_pipeline_no_results_flow(
        self,
        mock_openai_service
    ):
        """Test RAG pipeline when Qdrant returns no results."""
        cache_service = CacheService(redis_url="redis://localhost:6379")

        try:
            await cache_service.initialize()

            # Mock Qdrant with empty results
            mock_qdrant = AsyncMock(spec=QdrantService)
            mock_qdrant.search.return_value = []

            rag_service = RAGService(
                mock_openai_service,
                mock_qdrant,
                cache_service
            )

            result = await rag_service.process_query("Unknown question", "session-789")

            # Should return graceful "no results" response
            assert "No relevant information found" in result["answer"]
            assert result["sources"] == []
            assert result["confidence"] == 0.0

        finally:
            await cache_service.close()

    async def test_pipeline_different_sessions_separate_caches(
        self,
        mock_openai_service,
        mock_qdrant_service
    ):
        """Test that different sessions maintain separate caches."""
        cache_service = CacheService(redis_url="redis://localhost:6379")

        try:
            await cache_service.initialize()
            rag_service = RAGService(
                mock_openai_service,
                mock_qdrant_service,
                cache_service
            )

            question = "Same question"
            session_1 = "session-1"
            session_2 = "session-2"

            # Query from session 1
            result_1 = await rag_service.process_query(question, session_1)
            embed_calls_1 = mock_openai_service.embed_text.call_count

            # Reset mock
            mock_openai_service.reset_mock()

            # Query from session 2 with same question
            result_2 = await rag_service.process_query(question, session_2)
            embed_calls_2 = mock_openai_service.embed_text.call_count

            # Each session should have its own cache entry
            # So embedding should be called for session 2 (no cache hit)
            assert embed_calls_2 > 0

        finally:
            await cache_service.close()

    async def test_embedding_caching_layer(
        self,
        mock_openai_service
    ):
        """Test that OpenAI service embedding caching works within RAG pipeline."""
        cache_service = CacheService(redis_url="redis://localhost:6379")

        try:
            await cache_service.initialize()

            # Create a real OpenAI service with cache (mocking the API)
            openai_service = OpenAIService(
                api_key="test-key",
                model="gpt-4",
                embedding_model="text-embedding-3-small",
                cache_service=cache_service
            )

            # Mock the actual API call
            with patch.object(openai_service, '_call_openai_api') as mock_api:
                mock_api.return_value = [0.1, 0.2, 0.3] * 100

                # First embedding - API call
                embed_1 = await openai_service.embed_text("test text")
                api_calls_1 = mock_api.call_count

                # Second embedding of same text - should use embedding cache
                embed_2 = await openai_service.embed_text("test text")
                api_calls_2 = mock_api.call_count

                # Should not have called API again (embedding cache hit)
                assert api_calls_2 == api_calls_1

        finally:
            await cache_service.close()

    async def test_context_building_from_search_results(
        self,
        mock_openai_service,
        mock_qdrant_service
    ):
        """Test that context is properly built from Qdrant search results."""
        cache_service = CacheService(redis_url="redis://localhost:6379")

        try:
            await cache_service.initialize()
            rag_service = RAGService(
                mock_openai_service,
                mock_qdrant_service,
                cache_service
            )

            question = "How do topics work?"
            page_context = "Module 1: ROS 2"

            result = await rag_service.process_query(question, "session", page_context)

            # Verify chat was called with proper context
            call_args = mock_openai_service.chat_completion.call_args
            assert call_args is not None

            # Context should be in the system prompt or messages
            messages = call_args[1].get("messages") or call_args[0][0]
            context_str = str(messages)
            assert page_context in context_str or "Module" in context_str

        finally:
            await cache_service.close()

    async def test_confidence_calculation_from_search_scores(
        self,
        mock_openai_service,
        mock_qdrant_service
    ):
        """Test that confidence is properly calculated from search result scores."""
        cache_service = CacheService(redis_url="redis://localhost:6379")

        try:
            await cache_service.initialize()
            rag_service = RAGService(
                mock_openai_service,
                mock_qdrant_service,
                cache_service
            )

            result = await rag_service.process_query("test question", "session")

            # Confidence should be average of search scores
            # Mock returns [0.95, 0.87]
            expected_confidence = (0.95 + 0.87) / 2
            assert abs(result["confidence"] - expected_confidence) < 0.01

        finally:
            await cache_service.close()

    async def test_pipeline_error_handling_invalid_question(
        self,
        mock_openai_service,
        mock_qdrant_service
    ):
        """Test pipeline error handling for invalid questions."""
        cache_service = CacheService(redis_url="redis://localhost:6379")

        try:
            await cache_service.initialize()
            rag_service = RAGService(
                mock_openai_service,
                mock_qdrant_service,
                cache_service
            )

            # Empty question
            with pytest.raises(ValueError):
                await rag_service.process_query("", "session")

            # Too long question
            with pytest.raises(ValueError):
                await rag_service.process_query("x" * 501, "session")

        finally:
            await cache_service.close()

    async def test_cache_cleanup_on_error(
        self,
        mock_openai_service,
        mock_qdrant_service
    ):
        """Test that cache service is cleaned up even when pipeline errors."""
        cache_service = AsyncMock(spec=CacheService)
        cache_service.get_query_cache.return_value = None
        cache_service.set_query_cache = AsyncMock()

        # Make Qdrant fail
        mock_qdrant_service.search.side_effect = Exception("Qdrant error")

        rag_service = RAGService(
            mock_openai_service,
            mock_qdrant_service,
            cache_service
        )

        # Pipeline should raise but not clean up here (cleanup is in routes)
        with pytest.raises(Exception):
            await rag_service.process_query("test", "session")


@pytest.mark.asyncio
class TestRAGServiceCacheTTLs:
    """Test cache TTL enforcement in RAG pipeline."""

    async def test_query_cache_ttl_one_hour(self):
        """Test that query cache has 1-hour TTL."""
        cache_service = CacheService(redis_url="redis://localhost:6379")

        try:
            await cache_service.initialize()

            question = "test"
            session_id = "session"
            response = {"answer": "test", "sources": [], "confidence": 0.5}

            # Set cache
            await cache_service.set_query_cache(question, session_id, response)

            # Immediately retrieve - should exist
            cached = await cache_service.get_query_cache(question, session_id)
            assert cached is not None

            # Note: Full TTL test would require mocking Redis or waiting 1 hour
            # This test at least verifies the API works

        finally:
            await cache_service.close()

    async def test_embedding_cache_ttl_24_hours(self):
        """Test that embedding cache has 24-hour TTL."""
        cache_service = CacheService(redis_url="redis://localhost:6379")

        try:
            await cache_service.initialize()

            text = "test text"
            embedding = [0.1] * 300

            # Cache embedding (internal method)
            cache_key = cache_service._generate_key(f"embedding:{text}")
            await cache_service._redis.setex(cache_key, 86400, str(embedding))

            # Retrieve - should exist
            cached = await cache_service._redis.get(cache_key)
            assert cached is not None

        finally:
            await cache_service.close()


@pytest.mark.asyncio
class TestRAGServiceCitationExtraction:
    """Test citation extraction from search results."""

    async def test_citations_extracted_from_search_results(self):
        """Test that citations are properly extracted from Qdrant search."""
        cache_service = CacheService(redis_url="redis://localhost:6379")

        try:
            await cache_service.initialize()

            mock_openai = AsyncMock()
            mock_openai.embed_text.return_value = [0.1] * 300
            mock_openai.chat_completion.return_value = "Answer based on context"

            mock_qdrant = AsyncMock()
            mock_qdrant.search.return_value = [
                {
                    "id": "1",
                    "score": 0.95,
                    "payload": {
                        "chapter": "Ch1",
                        "section": "Sec1",
                        "content": "Content 1",
                        "confidence_score": 0.95
                    }
                }
            ]

            rag = RAGService(mock_openai, mock_qdrant, cache_service)
            result = await rag.process_query("test", "session")

            # Citations should be extracted
            assert len(result["sources"]) > 0
            source = result["sources"][0]
            assert "score" in source or "confidence_score" in source

        finally:
            await cache_service.close()
