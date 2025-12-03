"""Rate limiting service using Token Bucket algorithm"""

import asyncio
import time
import logging
from typing import Dict, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class TokenBucket:
    """Token bucket for rate limiting"""
    capacity: int  # Maximum tokens
    refill_rate: float  # Tokens per second
    tokens: float  # Current tokens
    last_refill: float  # Last refill timestamp


class RateLimiter:
    """Rate limiter using Token Bucket algorithm per session"""

    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        """Initialize rate limiter

        Args:
            max_requests: Maximum requests allowed per window (default: 60)
            window_seconds: Time window in seconds (default: 60)
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.refill_rate = max_requests / window_seconds  # tokens per second
        self.buckets: Dict[str, TokenBucket] = {}
        self._lock = asyncio.Lock()

    async def is_allowed(self, session_id: str) -> Tuple[bool, Dict]:
        """Check if request is allowed for session

        Args:
            session_id: Session identifier

        Returns:
            Tuple of (allowed: bool, headers: dict with rate limit info)
        """
        async with self._lock:
            current_time = time.time()

            # Create bucket for new session
            if session_id not in self.buckets:
                self.buckets[session_id] = TokenBucket(
                    capacity=self.max_requests,
                    refill_rate=self.refill_rate,
                    tokens=float(self.max_requests),
                    last_refill=current_time
                )

            bucket = self.buckets[session_id]

            # Refill tokens based on time elapsed
            elapsed = current_time - bucket.last_refill
            tokens_to_add = elapsed * bucket.refill_rate
            bucket.tokens = min(bucket.capacity, bucket.tokens + tokens_to_add)
            bucket.last_refill = current_time

            # Check if we have tokens available
            allowed = bucket.tokens >= 1

            if allowed:
                bucket.tokens -= 1
                remaining = int(bucket.tokens)
            else:
                remaining = 0
                # Calculate when the next token will be available
                tokens_needed = 1 - bucket.tokens
                wait_seconds = tokens_needed / bucket.refill_rate

            headers = {
                "X-RateLimit-Limit": str(self.max_requests),
                "X-RateLimit-Remaining": str(remaining),
                "X-RateLimit-Reset": str(int(bucket.last_refill + self.window_seconds)),
            }

            if not allowed:
                retry_after = int(wait_seconds) + 1
                headers["Retry-After"] = str(retry_after)
                logger.warning(
                    f"Rate limit exceeded for session {session_id}. "
                    f"Retry after {retry_after} seconds"
                )

            return allowed, headers

    async def cleanup_expired(self, max_age_seconds: int = 86400):
        """Clean up buckets older than max_age (default: 24 hours)

        Args:
            max_age_seconds: Maximum age of bucket in seconds
        """
        async with self._lock:
            current_time = time.time()
            expired_sessions = []

            for session_id, bucket in self.buckets.items():
                age = current_time - bucket.last_refill
                if age > max_age_seconds:
                    expired_sessions.append(session_id)

            for session_id in expired_sessions:
                del self.buckets[session_id]
                logger.debug(f"Cleaned up expired rate limit bucket for session {session_id}")

            return len(expired_sessions)

    def get_stats(self, session_id: str) -> Dict:
        """Get rate limit stats for a session

        Args:
            session_id: Session identifier

        Returns:
            Stats dictionary
        """
        if session_id not in self.buckets:
            return {"status": "no_bucket"}

        bucket = self.buckets[session_id]
        return {
            "tokens": round(bucket.tokens, 2),
            "capacity": bucket.capacity,
            "requests_remaining": int(bucket.tokens),
            "last_refill": bucket.last_refill,
        }
