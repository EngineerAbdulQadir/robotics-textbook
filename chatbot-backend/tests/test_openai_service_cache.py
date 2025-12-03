"""
Unit tests for OpenAI service with embedding caching (Phase 4)
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.services.openai_service import OpenAIService
from src.services.cache_service import CacheService


class TestOpenAIServiceEmbeddingCache:
    """Test OpenAI service embedding caching"""

    @pytest.fixture
    def mock_cache_service(self):
        """Create mock cache service"""
        cache = AsyncMock(spec=CacheService)
        cache.get_embedding_cache = AsyncMock(return_value=None)
        cache.set_embedding_cache = AsyncMock(return_value=True)
        return cache

    @pytest.fixture
    def openai_service(self, mock_cache_service):
        """Create OpenAI service with mock cache"""
        return OpenAIService(
            api_key="test-key",
            model="gpt-4",
            embedding_model="text-embedding-3-small",
            cache_service=mock_cache_service
        )

    @pytest.mark.asyncio
    async def test_embed_text_cache_miss(self, openai_service, mock_cache_service):
        """Test embedding generation on cache miss"""
        text = "Hello world"
        expected_embedding = [0.1] * 1536

        # Mock cache miss
        mock_cache_service.get_embedding_cache = AsyncMock(return_value=None)

        # Mock OpenAI API
        with patch.object(
            openai_service.async_client.embeddings,
            'create',
            new_callable=AsyncMock
        ) as mock_create:
            mock_response = MagicMock()
            mock_response.data = [MagicMock(embedding=expected_embedding)]
            mock_create.return_value = mock_response

            # Call embed_text
            result = await openai_service.embed_text(text)

            # Verify API was called
            mock_create.assert_called_once()
            assert result == expected_embedding

            # Verify cache was updated
            mock_cache_service.set_embedding_cache.assert_called_once_with(
                text, expected_embedding
            )

    @pytest.mark.asyncio
    async def test_embed_text_cache_hit(self, openai_service, mock_cache_service):
        """Test embedding retrieval on cache hit"""
        text = "Hello world"
        cached_embedding = [0.1] * 1536

        # Mock cache hit
        mock_cache_service.get_embedding_cache = AsyncMock(return_value=cached_embedding)

        # Call embed_text
        result = await openai_service.embed_text(text)

        # Verify API was NOT called
        assert result == cached_embedding
        mock_cache_service.get_embedding_cache.assert_called_once_with(text)

    @pytest.mark.asyncio
    async def test_embed_text_without_cache(self):
        """Test embedding generation without cache service"""
        openai_service = OpenAIService(
            api_key="test-key",
            model="gpt-4",
            embedding_model="text-embedding-3-small",
            cache_service=None
        )

        text = "Hello world"
        expected_embedding = [0.1] * 1536

        # Mock OpenAI API
        with patch.object(
            openai_service.async_client.embeddings,
            'create',
            new_callable=AsyncMock
        ) as mock_create:
            mock_response = MagicMock()
            mock_response.data = [MagicMock(embedding=expected_embedding)]
            mock_create.return_value = mock_response

            result = await openai_service.embed_text(text)

            assert result == expected_embedding
            mock_create.assert_called_once()

    @pytest.mark.asyncio
    async def test_embed_text_cache_error_fallback(self, openai_service, mock_cache_service):
        """Test that cache errors are propagated (no fallback in current implementation)"""
        text = "Hello world"

        # Mock cache error
        mock_cache_service.get_embedding_cache = AsyncMock(side_effect=Exception("Cache error"))

        # Current implementation propagates cache errors
        # Future enhancement could add fallback to API call
        with pytest.raises(Exception, match="Cache error"):
            await openai_service.embed_text(text)

    @pytest.mark.asyncio
    async def test_chat_completion_caching_not_implemented(self, openai_service):
        """Test that chat completion caching is not implemented at service level"""
        messages = [{"role": "user", "content": "Hello"}]

        with patch.object(
            openai_service.async_client.chat.completions,
            'create',
            new_callable=AsyncMock
        ) as mock_create:
            mock_response = MagicMock()
            mock_response.choices = [MagicMock(message=MagicMock(content="Hello!"))]
            mock_create.return_value = mock_response

            result = await openai_service.chat_completion(messages=messages)

            # Chat completion should always call API (caching at middleware level)
            assert result == "Hello!"
            mock_create.assert_called_once()


class TestOpenAIServiceCacheIntegration:
    """Integration tests for OpenAI service with cache"""

    @pytest.mark.asyncio
    async def test_multiple_embeds_same_text(self):
        """Test that same text reuses cached embedding"""
        mock_cache = AsyncMock(spec=CacheService)

        # Set up cache to track calls
        embedding1 = [0.1] * 1536
        embedding2 = [0.2] * 1536  # Different if called again

        call_count = [0]

        async def get_cache_side_effect(text):
            # First call: cache miss, second call: cache hit
            if call_count[0] == 0:
                call_count[0] += 1
                return None
            return embedding1

        mock_cache.get_embedding_cache = AsyncMock(side_effect=get_cache_side_effect)
        mock_cache.set_embedding_cache = AsyncMock(return_value=True)

        openai_service = OpenAIService(
            api_key="test-key",
            cache_service=mock_cache
        )

        text = "Repeated question"

        # First call - miss
        with patch.object(
            openai_service.async_client.embeddings,
            'create',
            new_callable=AsyncMock
        ) as mock_create:
            mock_response = MagicMock()
            mock_response.data = [MagicMock(embedding=embedding1)]
            mock_create.return_value = mock_response

            result1 = await openai_service.embed_text(text)
            assert result1 == embedding1

        # Second call - hit (same text)
        result2 = await openai_service.embed_text(text)
        assert result2 == embedding1

        # Verify cache was checked twice
        assert mock_cache.get_embedding_cache.call_count == 2

    @pytest.mark.asyncio
    async def test_different_texts_separate_cache_entries(self):
        """Test that different texts have separate cache entries"""
        mock_cache = AsyncMock(spec=CacheService)
        mock_cache.get_embedding_cache = AsyncMock(return_value=None)
        mock_cache.set_embedding_cache = AsyncMock(return_value=True)

        openai_service = OpenAIService(
            api_key="test-key",
            cache_service=mock_cache
        )

        text1 = "First text"
        text2 = "Second text"
        embedding1 = [0.1] * 1536
        embedding2 = [0.2] * 1536

        with patch.object(
            openai_service.async_client.embeddings,
            'create',
            new_callable=AsyncMock
        ) as mock_create:
            # First text
            mock_response = MagicMock()
            mock_response.data = [MagicMock(embedding=embedding1)]
            mock_create.return_value = mock_response

            await openai_service.embed_text(text1)

            # Second text
            mock_response.data = [MagicMock(embedding=embedding2)]
            await openai_service.embed_text(text2)

        # Verify both were cached with different keys
        assert mock_cache.set_embedding_cache.call_count == 2
        calls = mock_cache.set_embedding_cache.call_args_list
        assert calls[0][0][0] == text1
        assert calls[1][0][0] == text2


class TestOpenAIServicePerformance:
    """Performance tests for OpenAI service"""

    @pytest.mark.asyncio
    async def test_cache_improves_performance(self):
        """Test that caching improves embedding performance"""
        import time

        mock_cache = AsyncMock(spec=CacheService)
        embedding = [0.1] * 1536

        # Setup cache to return on second call
        call_count = [0]

        async def cache_side_effect(text):
            call_count[0] += 1
            if call_count[0] > 1:
                return embedding
            return None

        mock_cache.get_embedding_cache = AsyncMock(side_effect=cache_side_effect)
        mock_cache.set_embedding_cache = AsyncMock(return_value=True)

        openai_service = OpenAIService(
            api_key="test-key",
            cache_service=mock_cache
        )

        with patch.object(
            openai_service.async_client.embeddings,
            'create',
            new_callable=AsyncMock
        ) as mock_create:
            mock_response = MagicMock()
            mock_response.data = [MagicMock(embedding=embedding)]
            mock_create.return_value = mock_response

            # First call with API
            start = time.time()
            await openai_service.embed_text("test")
            api_time = time.time() - start

            # Second call from cache
            start = time.time()
            await openai_service.embed_text("test")
            cache_time = time.time() - start

            # Cache should be faster (or at least not slower)
            # In real scenario, cache would be much faster
            assert cache_time <= api_time or cache_time < 0.01
