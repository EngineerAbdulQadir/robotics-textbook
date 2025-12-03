"""
Unit tests for cache service (Phase 4)
"""

import pytest
import json
from unittest.mock import AsyncMock, MagicMock, patch
from src.services.cache_service import CacheService


class TestCacheService:
    """Test cache service functionality"""

    @pytest.fixture
    def cache_service(self):
        """Create cache service instance for testing"""
        return CacheService(redis_url="redis://localhost:6379")

    @pytest.mark.asyncio
    async def test_cache_service_initialization(self, cache_service):
        """Test cache service initializes"""
        assert cache_service.redis_url == "redis://localhost:6379"
        assert cache_service.redis is None

    @pytest.mark.asyncio
    async def test_key_generation(self, cache_service):
        """Test cache key generation with MD5 hashing"""
        key1 = cache_service._generate_key("query", "What is AI?", "session-1")
        key2 = cache_service._generate_key("query", "What is AI?", "session-1")
        key3 = cache_service._generate_key("query", "What is ML?", "session-1")

        # Same inputs should generate same key
        assert key1 == key2

        # Different inputs should generate different key
        assert key1 != key3

        # Key should be MD5 hash (32 hex characters)
        assert len(key1) == 32
        assert all(c in "0123456789abcdef" for c in key1)

    @pytest.mark.asyncio
    async def test_query_cache_operations(self, cache_service):
        """Test query cache operations"""
        # Mock Redis
        cache_service.redis = AsyncMock()

        question = "What is machine learning?"
        session_id = "test-session"
        cache_result = {
            "answer": "ML is a subset of AI",
            "sources": [],
            "confidence": 0.85
        }

        # Test cache miss
        cache_service.redis.get = AsyncMock(return_value=None)
        result = await cache_service.get_query_cache(question, session_id)
        assert result is None

        # Test cache hit
        cache_service.redis.get = AsyncMock(return_value=json.dumps(cache_result))
        result = await cache_service.get_query_cache(question, session_id)
        assert result == cache_result

        # Test cache set
        cache_service.redis.setex = AsyncMock()
        success = await cache_service.set_query_cache(question, session_id, cache_result)
        assert success is True
        cache_service.redis.setex.assert_called_once()

    @pytest.mark.asyncio
    async def test_embedding_cache_operations(self, cache_service):
        """Test embedding cache operations"""
        # Mock Redis
        cache_service.redis = AsyncMock()

        text = "Hello world"
        embedding = [0.1, 0.2, 0.3, 0.4, 0.5]

        # Test cache miss
        cache_service.redis.get = AsyncMock(return_value=None)
        result = await cache_service.get_embedding_cache(text)
        assert result is None

        # Test cache hit
        cache_service.redis.get = AsyncMock(return_value=json.dumps(embedding))
        result = await cache_service.get_embedding_cache(text)
        assert result == embedding

        # Test cache set
        cache_service.redis.setex = AsyncMock()
        success = await cache_service.set_embedding_cache(text, embedding)
        assert success is True
        # Check TTL is 24 hours
        call_args = cache_service.redis.setex.call_args
        assert call_args[0][1] == 86400  # 24 hours in seconds

    @pytest.mark.asyncio
    async def test_query_cache_ttl(self, cache_service):
        """Test query cache TTL is 1 hour"""
        cache_service.redis = AsyncMock()
        cache_service.redis.setex = AsyncMock()

        question = "Test question"
        session_id = "test-session"
        result = {"answer": "test"}

        await cache_service.set_query_cache(question, session_id, result)

        # Check TTL is 1 hour (3600 seconds)
        call_args = cache_service.redis.setex.call_args
        ttl = call_args[0][1]
        assert ttl == 3600

    @pytest.mark.asyncio
    async def test_embedding_cache_ttl(self, cache_service):
        """Test embedding cache TTL is 24 hours"""
        cache_service.redis = AsyncMock()
        cache_service.redis.setex = AsyncMock()

        text = "Test text"
        embedding = [0.1, 0.2]

        await cache_service.set_embedding_cache(text, embedding)

        # Check TTL is 24 hours
        call_args = cache_service.redis.setex.call_args
        ttl = call_args[0][1]
        assert ttl == 86400  # 24 hours

    @pytest.mark.asyncio
    async def test_cache_initialization(self, cache_service):
        """Test cache service initialization"""
        with patch('redis.asyncio.from_url') as mock_redis:
            mock_redis.return_value = AsyncMock()
            await cache_service.initialize()
            mock_redis.assert_called_once()

    @pytest.mark.asyncio
    async def test_cache_close(self, cache_service):
        """Test cache service closure"""
        cache_service.redis = AsyncMock()
        await cache_service.close()
        cache_service.redis.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_health_check_healthy(self, cache_service):
        """Test health check when Redis is healthy"""
        cache_service.redis = AsyncMock()
        cache_service.redis.ping = AsyncMock(return_value=True)

        healthy = await cache_service.health_check()
        assert healthy is True

    @pytest.mark.asyncio
    async def test_health_check_unhealthy(self, cache_service):
        """Test health check when Redis is unhealthy"""
        cache_service.redis = AsyncMock()
        cache_service.redis.ping = AsyncMock(side_effect=Exception("Connection failed"))

        healthy = await cache_service.health_check()
        assert healthy is False

    @pytest.mark.asyncio
    async def test_health_check_no_redis(self, cache_service):
        """Test health check when Redis is not initialized"""
        cache_service.redis = None

        healthy = await cache_service.health_check()
        assert healthy is False

    @pytest.mark.asyncio
    async def test_get_error_handling(self, cache_service):
        """Test get operation error handling"""
        cache_service.redis = AsyncMock()
        cache_service.redis.get = AsyncMock(side_effect=Exception("Redis error"))

        result = await cache_service.get("test-key")
        assert result is None

    @pytest.mark.asyncio
    async def test_set_error_handling(self, cache_service):
        """Test set operation error handling"""
        cache_service.redis = AsyncMock()
        cache_service.redis.setex = AsyncMock(side_effect=Exception("Redis error"))

        success = await cache_service.set("test-key", {"data": "test"}, ttl=3600)
        assert success is False

    @pytest.mark.asyncio
    async def test_delete_operation(self, cache_service):
        """Test delete operation"""
        cache_service.redis = AsyncMock()
        cache_service.redis.delete = AsyncMock()

        success = await cache_service.delete("test-key")
        assert success is True
        cache_service.redis.delete.assert_called_once_with("test-key")

    @pytest.mark.asyncio
    async def test_delete_error_handling(self, cache_service):
        """Test delete error handling"""
        cache_service.redis = AsyncMock()
        cache_service.redis.delete = AsyncMock(side_effect=Exception("Redis error"))

        success = await cache_service.delete("test-key")
        assert success is False

    @pytest.mark.asyncio
    async def test_cache_json_serialization(self, cache_service):
        """Test JSON serialization of cached values"""
        cache_service.redis = AsyncMock()

        complex_data = {
            "answer": "Test answer",
            "sources": [
                {"id": "1", "score": 0.95, "text": "Source 1"},
                {"id": "2", "score": 0.87, "text": "Source 2"}
            ],
            "confidence": 0.91
        }

        # Mock redis.setex to capture the value
        cache_service.redis.setex = AsyncMock()
        await cache_service.set("test-key", complex_data, ttl=3600)

        # Check that value was JSON serialized
        call_args = cache_service.redis.setex.call_args
        stored_value = call_args[0][2]
        assert isinstance(stored_value, str)
        assert json.loads(stored_value) == complex_data


class TestCacheServiceIntegration:
    """Integration tests for cache service with mocked Redis"""

    @pytest.mark.asyncio
    async def test_query_cache_full_flow(self):
        """Test complete query cache flow"""
        cache_service = CacheService(redis_url="redis://localhost:6379")
        cache_service.redis = AsyncMock()

        question = "What is deep learning?"
        session_id = "session-123"
        response = {
            "answer": "Deep learning is...",
            "sources": [],
            "confidence": 0.88
        }

        # First call - miss
        cache_service.redis.get = AsyncMock(return_value=None)
        result = await cache_service.get_query_cache(question, session_id)
        assert result is None

        # Save to cache
        cache_service.redis.setex = AsyncMock()
        await cache_service.set_query_cache(question, session_id, response)

        # Second call - hit
        cache_service.redis.get = AsyncMock(return_value=json.dumps(response))
        result = await cache_service.get_query_cache(question, session_id)
        assert result == response

    @pytest.mark.asyncio
    async def test_embedding_cache_full_flow(self):
        """Test complete embedding cache flow"""
        cache_service = CacheService(redis_url="redis://localhost:6379")
        cache_service.redis = AsyncMock()

        text = "Neural networks"
        embedding = [0.1] * 1536  # text-embedding-3-small dimension

        # First call - miss
        cache_service.redis.get = AsyncMock(return_value=None)
        result = await cache_service.get_embedding_cache(text)
        assert result is None

        # Save to cache
        cache_service.redis.setex = AsyncMock()
        await cache_service.set_embedding_cache(text, embedding)

        # Second call - hit
        cache_service.redis.get = AsyncMock(return_value=json.dumps(embedding))
        result = await cache_service.get_embedding_cache(text)
        assert result == embedding
        assert len(result) == 1536
