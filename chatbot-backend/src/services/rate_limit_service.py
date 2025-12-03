"""Rate limiting service for API requests."""

import logging
import time
from typing import Optional
from datetime import datetime, timedelta
from collections import defaultdict

logger = logging.getLogger(__name__)


class TokenBucket:
    """Token bucket rate limiter."""

    def __init__(self, capacity: int, refill_rate: float):
        """
        Initialize token bucket.

        Args:
            capacity: Maximum tokens (requests per window)
            refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()

    def consume(self, tokens: int = 1) -> bool:
        """
        Try to consume tokens.

        Args:
            tokens: Number of tokens to consume

        Returns:
            True if tokens available, False if rate limited
        """
        # Refill tokens based on time elapsed
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(
            self.capacity,
            self.tokens + elapsed * self.refill_rate,
        )
        self.last_refill = now

        if self.tokens >= tokens:
            self.tokens -= tokens
            return True

        return False

    def get_reset_time(self) -> float:
        """Get time when next token will be available."""
        if self.tokens >= 1:
            return 0

        tokens_needed = 1 - self.tokens
        time_to_reset = tokens_needed / self.refill_rate
        return time_to_reset


class RateLimitService:
    """Service for rate limiting API requests."""

    # Default limits: 60 requests per minute
    DEFAULT_REQUESTS_PER_MINUTE = 60
    DEFAULT_REQUESTS_PER_HOUR = 1000

    def __init__(self):
        """Initialize rate limit service."""
        self.buckets = defaultdict(self._create_bucket)
        self.blocked_until = defaultdict(lambda: None)

    def _create_bucket(self) -> TokenBucket:
        """Create a new token bucket."""
        # 1 request per second (60 per minute)
        return TokenBucket(
            capacity=self.DEFAULT_REQUESTS_PER_MINUTE,
            refill_rate=self.DEFAULT_REQUESTS_PER_MINUTE / 60,
        )

    async def check_rate_limit(
        self,
        session_id: str,
        endpoint: str = "general",
    ) -> tuple[bool, Optional[float]]:
        """
        Check if request is within rate limit.

        Args:
            session_id: User session ID
            endpoint: API endpoint being called

        Returns:
            Tuple of (is_allowed, reset_time_in_seconds)
        """
        key = f"{session_id}:{endpoint}"

        # Check if session is temporarily blocked
        if self.blocked_until[key]:
            reset_time = self.blocked_until[key]
            if datetime.utcnow() < reset_time:
                time_remaining = (reset_time - datetime.utcnow()).total_seconds()
                logger.warning(f"⏱️ Rate limited: {key} ({time_remaining:.1f}s remaining)")
                return False, time_remaining

            # Unlock session
            self.blocked_until[key] = None

        # Try to consume token
        bucket = self.buckets[key]
        if bucket.consume(1):
            logger.debug(f"✓ Rate limit check passed: {key}")
            return True, None

        # Rate limit exceeded - block for a short time
        reset_time = datetime.utcnow() + timedelta(seconds=bucket.get_reset_time())
        self.blocked_until[key] = reset_time
        time_remaining = bucket.get_reset_time()

        logger.warning(f"❌ Rate limit exceeded: {key}")
        return False, time_remaining

    def get_limit_headers(self, session_id: str) -> dict:
        """Get rate limit headers for response."""
        key = f"{session_id}:general"
        bucket = self.buckets[key]

        return {
            "X-RateLimit-Limit": str(self.DEFAULT_REQUESTS_PER_MINUTE),
            "X-RateLimit-Remaining": str(int(bucket.tokens)),
            "X-RateLimit-Reset": str(int(bucket.last_refill + 60)),
        }

    async def reset_session_limits(self, session_id: str) -> None:
        """Reset rate limits for a session."""
        # Remove all buckets for this session
        keys_to_remove = [
            k for k in self.buckets.keys()
            if k.startswith(session_id)
        ]
        for key in keys_to_remove:
            del self.buckets[key]
            if key in self.blocked_until:
                del self.blocked_until[key]

        logger.info(f"✓ Reset rate limits for session: {session_id}")

    def get_stats(self) -> dict:
        """Get rate limiting statistics."""
        active_sessions = len(set(k.split(":")[0] for k in self.buckets.keys()))
        blocked_sessions = sum(
            1 for v in self.blocked_until.values()
            if v and v > datetime.utcnow()
        )

        return {
            "active_sessions": active_sessions,
            "blocked_sessions": blocked_sessions,
            "total_buckets": len(self.buckets),
        }


# Global instance
_rate_limit_service = None


def get_rate_limit_service() -> RateLimitService:
    """Get or create rate limit service instance."""
    global _rate_limit_service
    if _rate_limit_service is None:
        _rate_limit_service = RateLimitService()
    return _rate_limit_service
