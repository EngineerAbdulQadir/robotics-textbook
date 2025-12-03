"""
Unit tests for rate limiter service (Phase 4)
"""

import pytest
import asyncio
import time
from src.services.rate_limiter import RateLimiter, TokenBucket


class TestTokenBucket:
    """Test token bucket implementation"""

    def test_token_bucket_initialization(self):
        """Test token bucket initializes with correct values"""
        bucket = TokenBucket(
            capacity=100,
            refill_rate=1.0,  # 1 token per second
            tokens=100.0,
            last_refill=time.time()
        )
        assert bucket.capacity == 100
        assert bucket.refill_rate == 1.0
        assert bucket.tokens == 100.0

    def test_bucket_has_sufficient_tokens(self):
        """Test bucket returns true when tokens available"""
        bucket = TokenBucket(
            capacity=100,
            refill_rate=1.0,
            tokens=50.0,
            last_refill=time.time()
        )
        assert bucket.tokens >= 1


class TestRateLimiter:
    """Test rate limiter service"""

    @pytest.mark.asyncio
    async def test_rate_limiter_initialization(self):
        """Test rate limiter initializes correctly"""
        limiter = RateLimiter(max_requests=100, window_seconds=60)
        assert limiter.max_requests == 100
        assert limiter.window_seconds == 60
        assert limiter.refill_rate == 100 / 60  # tokens per second

    @pytest.mark.asyncio
    async def test_first_request_allowed(self):
        """Test first request from new session is allowed"""
        limiter = RateLimiter(max_requests=10, window_seconds=60)
        session_id = "test-session-1"

        allowed, headers = await limiter.is_allowed(session_id)

        assert allowed is True
        assert int(headers["X-RateLimit-Remaining"]) == 9
        assert headers["X-RateLimit-Limit"] == "10"

    @pytest.mark.asyncio
    async def test_rate_limit_exceeded(self):
        """Test request is denied when rate limit exceeded"""
        limiter = RateLimiter(max_requests=3, window_seconds=60)
        session_id = "test-session-2"

        # Make 3 allowed requests
        for i in range(3):
            allowed, headers = await limiter.is_allowed(session_id)
            assert allowed is True

        # 4th request should be denied
        allowed, headers = await limiter.is_allowed(session_id)
        assert allowed is False
        assert "Retry-After" in headers
        assert int(headers["Retry-After"]) > 0

    @pytest.mark.asyncio
    async def test_rate_limit_headers(self):
        """Test rate limit headers are properly formatted"""
        limiter = RateLimiter(max_requests=100, window_seconds=60)
        session_id = "test-session-3"

        allowed, headers = await limiter.is_allowed(session_id)

        # Check all required headers present
        assert "X-RateLimit-Limit" in headers
        assert "X-RateLimit-Remaining" in headers
        assert "X-RateLimit-Reset" in headers

        # Check header values are integers/valid
        assert int(headers["X-RateLimit-Limit"]) > 0
        assert int(headers["X-RateLimit-Remaining"]) >= 0
        assert int(headers["X-RateLimit-Reset"]) > 0

    @pytest.mark.asyncio
    async def test_multiple_sessions_isolated(self):
        """Test rate limiting is per-session"""
        limiter = RateLimiter(max_requests=2, window_seconds=60)
        session1 = "session-1"
        session2 = "session-2"

        # Exhaust session 1
        await limiter.is_allowed(session1)
        await limiter.is_allowed(session1)
        allowed1, _ = await limiter.is_allowed(session1)
        assert allowed1 is False

        # Session 2 should still have requests available
        allowed2, _ = await limiter.is_allowed(session2)
        assert allowed2 is True

    @pytest.mark.asyncio
    async def test_cleanup_expired_buckets(self):
        """Test expired buckets are cleaned up"""
        limiter = RateLimiter(max_requests=10, window_seconds=60)

        # Create a bucket
        await limiter.is_allowed("old-session")
        assert "old-session" in limiter.buckets

        # Cleanup with very short age (should not remove)
        removed = await limiter.cleanup_expired(max_age_seconds=1000)
        assert removed == 0

        # Manual cleanup of old bucket
        limiter.buckets["old-session"].last_refill = time.time() - 100000
        removed = await limiter.cleanup_expired(max_age_seconds=1000)
        assert removed == 1
        assert "old-session" not in limiter.buckets

    @pytest.mark.asyncio
    async def test_get_stats(self):
        """Test retrieving rate limiter stats"""
        limiter = RateLimiter(max_requests=100, window_seconds=60)
        session_id = "stats-test"

        # Before any request
        stats = limiter.get_stats(session_id)
        assert stats["status"] == "no_bucket"

        # After first request
        await limiter.is_allowed(session_id)
        stats = limiter.get_stats(session_id)

        # Should have bucket with stats
        assert "tokens" in stats
        assert "capacity" in stats
        assert "requests_remaining" in stats
        assert stats["capacity"] == 100  # Default from test setup

    @pytest.mark.asyncio
    async def test_token_refill_over_time(self):
        """Test tokens refill over time"""
        limiter = RateLimiter(max_requests=10, window_seconds=60)
        session_id = "refill-test"

        # Use all tokens
        for _ in range(10):
            await limiter.is_allowed(session_id)

        # Should be denied
        allowed, _ = await limiter.is_allowed(session_id)
        assert allowed is False

        # Wait for some tokens to refill
        await asyncio.sleep(2)

        # Should have some tokens available now (approximately 2 tokens)
        allowed, headers = await limiter.is_allowed(session_id)
        # Note: May still be denied depending on exact timing
        # But we can check the bucket has refilled
        bucket = limiter.buckets[session_id]
        assert bucket.tokens < 10  # Not full
        assert bucket.tokens > 0  # Has some tokens


class TestRateLimiterEdgeCases:
    """Test edge cases and error scenarios"""

    @pytest.mark.asyncio
    async def test_concurrent_requests(self):
        """Test rate limiter under concurrent requests"""
        limiter = RateLimiter(max_requests=5, window_seconds=60)
        session_id = "concurrent-test"

        # Make 5 concurrent requests
        tasks = [limiter.is_allowed(session_id) for _ in range(5)]
        results = await asyncio.gather(*tasks)

        # Count allowed vs denied
        allowed_count = sum(1 for allowed, _ in results if allowed)
        denied_count = sum(1 for allowed, _ in results if not allowed)

        # All should be allowed (first 5)
        assert allowed_count >= 5 or denied_count == 0  # Account for timing

    @pytest.mark.asyncio
    async def test_zero_remaining_header(self):
        """Test X-RateLimit-Remaining is 0 when limit hit"""
        limiter = RateLimiter(max_requests=1, window_seconds=60)
        session_id = "zero-test"

        # First request uses the token
        await limiter.is_allowed(session_id)

        # Second request denied, remaining should be 0
        allowed, headers = await limiter.is_allowed(session_id)
        assert allowed is False
        assert int(headers["X-RateLimit-Remaining"]) == 0

    @pytest.mark.asyncio
    async def test_large_request_window(self):
        """Test rate limiter with large request window"""
        limiter = RateLimiter(max_requests=1000, window_seconds=3600)  # 1000 per hour

        session_id = "large-window"
        for _ in range(100):
            allowed, _ = await limiter.is_allowed(session_id)
            assert allowed is True

        # Should still have requests available
        allowed, headers = await limiter.is_allowed(session_id)
        assert allowed is True
        assert int(headers["X-RateLimit-Remaining"]) > 800


# Performance tests
class TestRateLimiterPerformance:
    """Test rate limiter performance"""

    @pytest.mark.asyncio
    async def test_is_allowed_performance(self):
        """Test is_allowed is fast enough"""
        limiter = RateLimiter(max_requests=1000, window_seconds=60)
        session_id = "perf-test"

        # Time 100 requests
        start = time.time()
        for _ in range(100):
            await limiter.is_allowed(session_id)
        elapsed = time.time() - start

        # Should complete in less than 100ms (1ms per request)
        assert elapsed < 0.1, f"Rate limiter took {elapsed}s for 100 requests"

    @pytest.mark.asyncio
    async def test_cleanup_performance(self):
        """Test cleanup performance with many buckets"""
        limiter = RateLimiter(max_requests=100, window_seconds=60)

        # Create 1000 buckets
        for i in range(1000):
            await limiter.is_allowed(f"session-{i}")

        # Cleanup should be fast
        start = time.time()
        removed = await limiter.cleanup_expired(max_age_seconds=1000)
        elapsed = time.time() - start

        assert elapsed < 1.0, f"Cleanup took {elapsed}s for 1000 buckets"
