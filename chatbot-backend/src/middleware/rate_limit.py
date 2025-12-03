"""Rate limiting middleware for FastAPI"""

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import logging
from typing import Callable

from ..services.rate_limiter import RateLimiter
from ..config import settings

logger = logging.getLogger(__name__)

# Global rate limiter instance
_rate_limiter: RateLimiter = None


def get_rate_limiter() -> RateLimiter:
    """Get or create global rate limiter instance"""
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RateLimiter(
            max_requests=settings.rate_limit_requests,
            window_seconds=settings.rate_limit_window_seconds
        )
    return _rate_limiter


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware to apply rate limiting based on session ID"""

    async def dispatch(self, request: Request, call_next: Callable) -> JSONResponse:
        """Apply rate limiting before processing request

        Rate limiting is applied to:
        - POST /api/v1/chat/query
        - POST /api/v1/chat/selection

        Session ID is extracted from:
        - Request body (for POST requests)
        - Query parameter ?session_id
        """
        # Skip rate limiting for non-chat endpoints
        if not request.url.path.startswith("/api/v1/chat/"):
            return await call_next(request)

        # Skip rate limiting for health checks and docs
        if request.url.path in ["/api/v1/health", "/api/v1/docs"]:
            return await call_next(request)

        # Extract session ID
        session_id = None

        # Try to get from query parameters
        session_id = request.query_params.get("session_id")

        # Try to get from request body (for POST requests)
        if not session_id and request.method == "POST":
            try:
                body = await request.body()
                if body:
                    import json
                    body_data = json.loads(body)
                    session_id = body_data.get("session_id")
                    # Re-set the body for the actual request handler
                    request._body = body
            except Exception as e:
                logger.debug(f"Could not parse request body for session ID: {e}")

        # Skip rate limiting if no session ID found
        if not session_id:
            logger.warning(
                f"No session ID found in request to {request.url.path}. "
                f"Skipping rate limiting."
            )
            return await call_next(request)

        # Check rate limit
        rate_limiter = get_rate_limiter()
        allowed, headers = await rate_limiter.is_allowed(session_id)

        if not allowed:
            logger.warning(f"Rate limit exceeded for session {session_id}")
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Rate limit exceeded. Too many requests.",
                    "status": "rate_limited",
                },
                headers=headers,
            )

        # Process request
        response = await call_next(request)

        # Add rate limit headers to response
        for key, value in headers.items():
            response.headers[key] = value

        logger.debug(
            f"Request allowed for session {session_id}. "
            f"Remaining: {headers.get('X-RateLimit-Remaining')}"
        )

        return response


async def cleanup_rate_limiter():
    """Cleanup expired rate limit buckets (call periodically)"""
    rate_limiter = get_rate_limiter()
    expired_count = await rate_limiter.cleanup_expired()
    if expired_count > 0:
        logger.info(f"Cleaned up {expired_count} expired rate limit buckets")
