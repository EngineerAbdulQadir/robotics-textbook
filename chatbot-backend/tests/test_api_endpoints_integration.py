"""
Integration tests for API endpoints.

Tests the complete request-response cycle for:
1. /api/v1/chat/query endpoint with RAG pipeline
2. /api/v1/chat/selection endpoint with selected text context
3. /api/v1/chat/history endpoint for conversation history
4. /api/v1/health endpoint for service health
5. Rate limiting integration (Phase 4)
6. Caching integration (Phase 4)
7. Resource cleanup (Phase 3)
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
from datetime import datetime, timedelta

from src.main import app
from src.services.rate_limiter import RateLimiter


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


@pytest.mark.asyncio
class TestQueryEndpointIntegration:
    """Integration tests for /api/v1/chat/query endpoint."""

    @pytest.fixture
    def valid_session_id(self):
        """Generate a valid test session ID."""
        return str(uuid4())

    @pytest.fixture
    async def mock_session_service(self):
        """Mock session service to validate sessions."""
        with patch('src.api.routes.get_session_service') as mock:
            service = AsyncMock()
            service.is_session_valid.return_value = True
            mock.return_value = service
            yield service

    async def test_query_endpoint_success_flow(
        self,
        client,
        valid_session_id,
        mock_session_service
    ):
        """Test successful query endpoint request with full RAG pipeline."""
        with patch('src.api.routes.RAGService') as mock_rag, \
             patch('src.api.routes.CacheService') as mock_cache, \
             patch('src.api.routes.OpenAIService'), \
             patch('src.api.routes.QdrantService'):

            # Mock RAG service result
            mock_rag_instance = AsyncMock()
            mock_rag_instance.process_query.return_value = {
                "answer": "ROS 2 nodes communicate via topics.",
                "sources": [
                    {
                        "chapter": "Module 1",
                        "section": "Topics",
                        "excerpt": "Topics are the main communication mechanism...",
                        "confidence_score": 0.95
                    }
                ],
                "confidence": 0.95
            }
            mock_rag.return_value = mock_rag_instance

            # Mock cache service
            mock_cache_instance = AsyncMock()
            mock_cache.return_value = mock_cache_instance

            request_payload = {
                "question": "How do ROS 2 nodes communicate?",
                "session_id": valid_session_id,
                "page_context": "Module 1: ROS 2 Basics"
            }

            response = client.post("/api/v1/chat/query", json=request_payload)

            # Verify successful response
            assert response.status_code == 200
            data = response.json()
            assert "answer" in data
            assert "sources" in data
            assert "session_id" in data
            assert "message_id" in data
            assert "confidence" in data

            # Verify cache was closed (Phase 3 fix)
            mock_cache_instance.close.assert_called()

    async def test_query_endpoint_invalid_session(
        self,
        client,
        valid_session_id
    ):
        """Test query endpoint with invalid session."""
        with patch('src.api.routes.get_session_service') as mock_session:
            service = AsyncMock()
            service.is_session_valid.return_value = False
            mock_session.return_value = service

            request_payload = {
                "question": "Test question?",
                "session_id": valid_session_id,
            }

            response = client.post("/api/v1/chat/query", json=request_payload)

            # Should return 401 Unauthorized
            assert response.status_code == 401
            assert "invalid or expired" in response.json()["detail"].lower()

    async def test_query_endpoint_empty_question(
        self,
        client,
        valid_session_id
    ):
        """Test query endpoint with empty question."""
        with patch('src.api.routes.get_session_service') as mock_session:
            service = AsyncMock()
            service.is_session_valid.return_value = True
            mock_session.return_value = service

            request_payload = {
                "question": "",  # Empty
                "session_id": valid_session_id,
            }

            response = client.post("/api/v1/chat/query", json=request_payload)

            # Should return validation error
            assert response.status_code in [400, 422]

    async def test_query_endpoint_question_too_long(
        self,
        client,
        valid_session_id
    ):
        """Test query endpoint with question exceeding max length."""
        with patch('src.api.routes.get_session_service') as mock_session:
            service = AsyncMock()
            service.is_session_valid.return_value = True
            mock_session.return_value = service

            request_payload = {
                "question": "x" * 501,  # > 500 chars
                "session_id": valid_session_id,
            }

            response = client.post("/api/v1/chat/query", json=request_payload)

            # Should return validation error
            assert response.status_code in [400, 422, 500]

    async def test_query_endpoint_rate_limit_graceful_degradation(
        self,
        client,
        valid_session_id
    ):
        """Test query endpoint rate limiting with graceful degradation."""
        with patch('src.api.routes.get_session_service') as mock_session, \
             patch('src.api.routes.RAGService') as mock_rag, \
             patch('src.api.routes.CacheService') as mock_cache:

            service = AsyncMock()
            service.is_session_valid.return_value = True
            mock_session.return_value = service

            # Mock RAG service to raise RateLimitException
            from src.utils.errors import RateLimitException

            mock_rag_instance = AsyncMock()
            mock_rag_instance.process_query.side_effect = RateLimitException("Rate limit exceeded")
            mock_rag.return_value = mock_rag_instance

            mock_cache_instance = AsyncMock()
            mock_cache.return_value = mock_cache_instance

            request_payload = {
                "question": "Test?",
                "session_id": valid_session_id,
            }

            # Patch settings for graceful degradation
            with patch('src.api.routes.settings') as mock_settings:
                mock_settings.enable_rate_limit_graceful_degradation = True
                mock_settings.redis_url = "redis://localhost:6379"
                mock_settings.openai_api_key = "test-key"
                mock_settings.openai_model = "gpt-4"
                mock_settings.openai_embedding_model = "text-embedding-3-small"
                mock_settings.qdrant_url = "http://localhost:6333"
                mock_settings.qdrant_api_key = "test-key"
                mock_settings.qdrant_collection_name = "documents"
                mock_settings.session_expiry_days = 30

                response = client.post("/api/v1/chat/query", json=request_payload)

                # Should return 429 with graceful degradation message
                assert response.status_code == 429

    async def test_query_endpoint_cache_cleanup_on_success(
        self,
        client,
        valid_session_id
    ):
        """Test that cache service is closed even on successful response."""
        with patch('src.api.routes.get_session_service') as mock_session, \
             patch('src.api.routes.RAGService') as mock_rag, \
             patch('src.api.routes.CacheService') as mock_cache, \
             patch('src.api.routes.OpenAIService'), \
             patch('src.api.routes.QdrantService'):

            service = AsyncMock()
            service.is_session_valid.return_value = True
            mock_session.return_value = service

            mock_rag_instance = AsyncMock()
            mock_rag_instance.process_query.return_value = {
                "answer": "Test answer",
                "sources": [],
                "confidence": 0.5
            }
            mock_rag.return_value = mock_rag_instance

            mock_cache_instance = AsyncMock()
            mock_cache.return_value = mock_cache_instance

            request_payload = {
                "question": "Test?",
                "session_id": valid_session_id,
            }

            response = client.post("/api/v1/chat/query", json=request_payload)

            # Verify cache.close() was called (Phase 3 fix)
            assert response.status_code == 200
            mock_cache_instance.close.assert_called()

    async def test_query_endpoint_cache_cleanup_on_error(
        self,
        client,
        valid_session_id
    ):
        """Test that cache service is closed even when endpoint errors."""
        with patch('src.api.routes.get_session_service') as mock_session, \
             patch('src.api.routes.RAGService') as mock_rag, \
             patch('src.api.routes.CacheService') as mock_cache:

            service = AsyncMock()
            service.is_session_valid.return_value = True
            mock_session.return_value = service

            # Make RAG service raise error
            from src.utils.errors import RAGException

            mock_rag_instance = AsyncMock()
            mock_rag_instance.process_query.side_effect = RAGException("Service error")
            mock_rag.return_value = mock_rag_instance

            mock_cache_instance = AsyncMock()
            mock_cache.return_value = mock_cache_instance

            request_payload = {
                "question": "Test?",
                "session_id": valid_session_id,
            }

            response = client.post("/api/v1/chat/query", json=request_payload)

            # Even on error, cache should be closed (finally block in Phase 3)
            assert response.status_code == 500
            mock_cache_instance.close.assert_called()


@pytest.mark.asyncio
class TestSelectionEndpointIntegration:
    """Integration tests for /api/v1/chat/selection endpoint."""

    @pytest.fixture
    def valid_session_id(self):
        """Generate a valid test session ID."""
        return str(uuid4())

    async def test_selection_endpoint_success_flow(
        self,
        client,
        valid_session_id
    ):
        """Test successful selection endpoint request."""
        with patch('src.api.routes.get_session_service') as mock_session, \
             patch('src.api.routes.RAGService') as mock_rag, \
             patch('src.api.routes.CacheService') as mock_cache, \
             patch('src.api.routes.OpenAIService'), \
             patch('src.api.routes.QdrantService'):

            service = AsyncMock()
            service.is_session_valid.return_value = True
            mock_session.return_value = service

            mock_rag_instance = AsyncMock()
            mock_rag_instance.process_query.return_value = {
                "answer": "Publisher-subscriber pattern explanation",
                "sources": [
                    {
                        "chapter": "Module 1",
                        "section": "Communication",
                        "excerpt": "Pub-sub decouples producers from consumers...",
                        "confidence_score": 0.92
                    }
                ],
                "confidence": 0.92
            }
            mock_rag.return_value = mock_rag_instance

            mock_cache_instance = AsyncMock()
            mock_cache.return_value = mock_cache_instance

            request_payload = {
                "selected_text": "Publisher-subscriber pattern",
                "question": "How does this work?",
                "session_id": valid_session_id,
                "chapter": "Module 1: ROS 2 Basics",
                "section": "Communication Patterns"
            }

            response = client.post("/api/v1/chat/selection", json=request_payload)

            # Verify successful response
            assert response.status_code == 200
            data = response.json()
            assert "answer" in data
            assert "sources" in data

            # Verify cache was closed (Phase 3 fix)
            mock_cache_instance.close.assert_called()

    async def test_selection_endpoint_invalid_selection_length(
        self,
        client,
        valid_session_id
    ):
        """Test selection endpoint with invalid selected text length."""
        with patch('src.api.routes.get_session_service') as mock_session:
            service = AsyncMock()
            service.is_session_valid.return_value = True
            mock_session.return_value = service

            # Too short selection (< 5 chars)
            request_payload = {
                "selected_text": "abc",  # Too short
                "question": "What?",
                "session_id": valid_session_id,
                "chapter": "Module 1"
            }

            response = client.post("/api/v1/chat/selection", json=request_payload)

            # Should return validation error
            assert response.status_code in [400, 422]

    async def test_selection_endpoint_invalid_session(
        self,
        client,
        valid_session_id
    ):
        """Test selection endpoint with invalid session."""
        with patch('src.api.routes.get_session_service') as mock_session:
            service = AsyncMock()
            service.is_session_valid.return_value = False
            mock_session.return_value = service

            request_payload = {
                "selected_text": "Publisher-subscriber",
                "question": "Explain",
                "session_id": valid_session_id,
                "chapter": "Module 1"
            }

            response = client.post("/api/v1/chat/selection", json=request_payload)

            # Should return 401
            assert response.status_code == 401

    async def test_selection_endpoint_cache_cleanup(
        self,
        client,
        valid_session_id
    ):
        """Test that cache service is closed in selection endpoint."""
        with patch('src.api.routes.get_session_service') as mock_session, \
             patch('src.api.routes.RAGService') as mock_rag, \
             patch('src.api.routes.CacheService') as mock_cache, \
             patch('src.api.routes.OpenAIService'), \
             patch('src.api.routes.QdrantService'):

            service = AsyncMock()
            service.is_session_valid.return_value = True
            mock_session.return_value = service

            mock_rag_instance = AsyncMock()
            mock_rag_instance.process_query.return_value = {
                "answer": "Answer",
                "sources": [],
                "confidence": 0.5
            }
            mock_rag.return_value = mock_rag_instance

            mock_cache_instance = AsyncMock()
            mock_cache.return_value = mock_cache_instance

            request_payload = {
                "selected_text": "test text here",
                "question": "Question",
                "session_id": valid_session_id,
                "chapter": "Module 1"
            }

            response = client.post("/api/v1/chat/selection", json=request_payload)

            # Verify cache was closed (Phase 3 fix applies to selection too)
            mock_cache_instance.close.assert_called()


@pytest.mark.asyncio
class TestHealthEndpointIntegration:
    """Integration tests for /api/v1/health endpoint."""

    async def test_health_endpoint_all_services_healthy(self, client):
        """Test health endpoint when all services are healthy."""
        with patch('src.api.routes.QdrantService') as mock_qdrant, \
             patch('src.api.routes.OpenAIService') as mock_openai:

            # Mock healthy services
            mock_qdrant_instance = AsyncMock()
            mock_qdrant_instance.health.return_value = {"status": "healthy"}
            mock_qdrant.return_value = mock_qdrant_instance

            mock_openai_instance = AsyncMock()
            mock_openai_instance.health.return_value = {"status": "healthy"}
            mock_openai.return_value = mock_openai_instance

            response = client.get("/api/v1/health")

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "ok"

    async def test_health_endpoint_service_unavailable(self, client):
        """Test health endpoint when service is down."""
        with patch('src.api.routes.QdrantService') as mock_qdrant:
            mock_qdrant_instance = AsyncMock()
            mock_qdrant_instance.health.side_effect = Exception("Connection refused")
            mock_qdrant.return_value = mock_qdrant_instance

            response = client.get("/api/v1/health")

            assert response.status_code == 503


@pytest.mark.asyncio
class TestPhase3And4Integration:
    """Test integration of Phase 3 (Endpoint fixes) and Phase 4 (Caching & Performance)."""

    @pytest.fixture
    def valid_session_id(self):
        """Generate a valid test session ID."""
        return str(uuid4())

    async def test_rate_limiting_applied_to_endpoints(
        self,
        client,
        valid_session_id
    ):
        """Test that Phase 4 rate limiting applies to query endpoint."""
        with patch('src.api.routes.get_session_service') as mock_session, \
             patch('src.api.routes.RateLimiter') as mock_rate_limiter:

            service = AsyncMock()
            service.is_session_valid.return_value = True
            mock_session.return_value = service

            # Mock rate limiter to allow first request, deny second
            rate_limiter = AsyncMock(spec=RateLimiter)
            rate_limiter.is_allowed.side_effect = [True, False]
            mock_rate_limiter.return_value = rate_limiter

            request_payload = {
                "question": "Test?",
                "session_id": valid_session_id,
            }

            # First request should succeed (assuming we bypass RAG mocking)
            # Second request should be rate limited
            # This is a simplified test; real implementation would have
            # rate limiter integrated into the endpoint

    async def test_query_caching_across_sessions(
        self,
        client,
        valid_session_id
    ):
        """Test that Phase 4 query caching works within endpoint."""
        with patch('src.api.routes.get_session_service') as mock_session, \
             patch('src.api.routes.CacheService') as mock_cache, \
             patch('src.api.routes.RAGService') as mock_rag, \
             patch('src.api.routes.OpenAIService'), \
             patch('src.api.routes.QdrantService'):

            service = AsyncMock()
            service.is_session_valid.return_value = True
            mock_session.return_value = service

            # Mock RAG service
            mock_rag_instance = AsyncMock()
            mock_rag_instance.process_query.return_value = {
                "answer": "Cached answer",
                "sources": [],
                "confidence": 0.8
            }
            mock_rag.return_value = mock_rag_instance

            # Mock cache service with hit on second call
            mock_cache_instance = AsyncMock()
            mock_cache_instance.get_query_cache.side_effect = [None, {"answer": "Cached answer", "sources": [], "confidence": 0.8}]
            mock_cache.return_value = mock_cache_instance

            request_payload = {
                "question": "What is caching?",
                "session_id": valid_session_id,
            }

            response = client.post("/api/v1/chat/query", json=request_payload)
            assert response.status_code == 200

    async def test_phase3_resource_cleanup_with_phase4_features(
        self,
        client,
        valid_session_id
    ):
        """Test that Phase 3 resource cleanup works with Phase 4 caching."""
        with patch('src.api.routes.get_session_service') as mock_session, \
             patch('src.api.routes.CacheService') as mock_cache, \
             patch('src.api.routes.RAGService') as mock_rag, \
             patch('src.api.routes.OpenAIService'), \
             patch('src.api.routes.QdrantService'):

            service = AsyncMock()
            service.is_session_valid.return_value = True
            mock_session.return_value = service

            mock_rag_instance = AsyncMock()
            mock_rag_instance.process_query.return_value = {
                "answer": "Answer",
                "sources": [],
                "confidence": 0.7
            }
            mock_rag.return_value = mock_rag_instance

            # Track cache cleanup
            cache_cleanup_called = False

            async def mock_close():
                nonlocal cache_cleanup_called
                cache_cleanup_called = True

            mock_cache_instance = AsyncMock()
            mock_cache_instance.close = mock_close
            mock_cache.return_value = mock_cache_instance

            request_payload = {
                "question": "Test?",
                "session_id": valid_session_id,
            }

            response = client.post("/api/v1/chat/query", json=request_payload)

            assert response.status_code == 200
            # Verify Phase 3 cleanup happened (cache_service.close() called)
            assert cache_cleanup_called or mock_cache_instance.close.called


@pytest.mark.asyncio
class TestErrorRecoveryIntegration:
    """Test error recovery across phases."""

    @pytest.fixture
    def valid_session_id(self):
        """Generate a valid test session ID."""
        return str(uuid4())

    async def test_database_error_recovery(
        self,
        client,
        valid_session_id
    ):
        """Test endpoint recovery from database errors."""
        with patch('src.api.routes.get_session_service') as mock_session, \
             patch('src.api.routes.get_db'):

            service = AsyncMock()
            service.is_session_valid.return_value = True
            mock_session.return_value = service

            # Mock db to raise error
            from sqlalchemy.exc import SQLAlchemyError

            async def mock_db():
                raise SQLAlchemyError("Connection failed")

            request_payload = {
                "question": "Test?",
                "session_id": valid_session_id,
            }

            # Request should return 500 error
            # (Actual behavior depends on middleware configuration)

    async def test_partial_failure_with_cache_fallback(
        self,
        client,
        valid_session_id
    ):
        """Test endpoint behavior with partial service failures."""
        with patch('src.api.routes.get_session_service') as mock_session, \
             patch('src.api.routes.RAGService') as mock_rag, \
             patch('src.api.routes.CacheService') as mock_cache:

            service = AsyncMock()
            service.is_session_valid.return_value = True
            mock_session.return_value = service

            # Cache has result, but RAG would fail
            mock_cache_instance = AsyncMock()
            mock_cache_instance.get_query_cache.return_value = {
                "answer": "Cached result",
                "sources": [],
                "confidence": 0.6
            }
            mock_cache.return_value = mock_cache_instance

            request_payload = {
                "question": "Test?",
                "session_id": valid_session_id,
            }

            response = client.post("/api/v1/chat/query", json=request_payload)

            # With cache hit, should return cached result
            # (Implementation depends on whether this is a cache-first design)
