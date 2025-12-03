"""Monitoring and logging middleware."""

import logging
import time
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class MonitoringMiddleware(BaseHTTPMiddleware):
    """Middleware for monitoring API requests and responses."""

    async def dispatch(self, request: Request, call_next):
        """Process request and log metrics."""
        # Start timer
        start_time = time.time()
        request_id = request.headers.get("X-Request-ID", str(time.time()))

        # Add request ID to request state
        request.state.request_id = request_id
        request.state.start_time = start_time

        try:
            # Log incoming request
            logger.info(
                f"→ {request.method} {request.url.path} "
                f"[{request_id}]"
            )

            # Process request
            response = await call_next(request)

            # Calculate duration
            duration = time.time() - start_time

            # Log outgoing response
            logger.info(
                f"← {response.status_code} {request.url.path} "
                f"({duration:.2f}s) [{request_id}]"
            )

            # Add monitoring headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Response-Time"] = f"{duration:.2f}s"

            return response

        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                f"❌ {request.method} {request.url.path} "
                f"({duration:.2f}s) - {e} [{request_id}]",
                exc_info=True,
            )
            raise


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for rate limiting."""

    def __init__(self, app, rate_limit_service=None):
        """Initialize rate limit middleware."""
        super().__init__(app)
        self.rate_limit_service = rate_limit_service

    async def dispatch(self, request: Request, call_next):
        """Check rate limits before processing request."""
        if not self.rate_limit_service:
            return await call_next(request)

        # Get session ID from request
        session_id = None
        if request.method == "POST":
            try:
                body = await request.body()
                import json
                data = json.loads(body)
                session_id = data.get("session_id")
            except:
                pass

        if session_id:
            # Check rate limit
            allowed, reset_time = await self.rate_limit_service.check_rate_limit(
                session_id,
                request.url.path,
            )

            if not allowed:
                logger.warning(f"Rate limited: {session_id}")
                return JSONResponse(
                    status_code=429,
                    content={
                        "detail": "Rate limit exceeded",
                        "retry_after": int(reset_time + 1),
                    },
                    headers={
                        "Retry-After": str(int(reset_time + 1)),
                        **self.rate_limit_service.get_limit_headers(session_id),
                    },
                )

        return await call_next(request)


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware for error handling."""

    async def dispatch(self, request: Request, call_next):
        """Handle errors and return consistent responses."""
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error(f"Unhandled error: {e}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={
                    "detail": "Internal server error",
                    "request_id": request.state.get("request_id"),
                },
            )
