"""Prometheus metrics service for monitoring"""

from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry, REGISTRY
import time
import logging
from typing import Optional, Callable
from functools import wraps

logger = logging.getLogger(__name__)

# Define metrics
query_latency = Histogram(
    'chatbot_query_latency_seconds',
    'Query processing latency in seconds',
    buckets=(0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
    registry=REGISTRY
)

query_count = Counter(
    'chatbot_queries_total',
    'Total number of queries processed',
    ['endpoint', 'status'],
    registry=REGISTRY
)

cache_hits = Counter(
    'chatbot_cache_hits_total',
    'Total cache hits',
    ['cache_type'],
    registry=REGISTRY
)

cache_misses = Counter(
    'chatbot_cache_misses_total',
    'Total cache misses',
    ['cache_type'],
    registry=REGISTRY
)

openai_api_calls = Counter(
    'chatbot_openai_api_calls_total',
    'Total OpenAI API calls',
    ['operation'],
    registry=REGISTRY
)

qdrant_searches = Counter(
    'chatbot_qdrant_searches_total',
    'Total Qdrant vector searches',
    registry=REGISTRY
)

qdrant_search_latency = Histogram(
    'chatbot_qdrant_search_latency_seconds',
    'Qdrant search latency',
    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5),
    registry=REGISTRY
)

rate_limit_hits = Counter(
    'chatbot_rate_limit_hits_total',
    'Total rate limit hits',
    ['session_id'],
    registry=REGISTRY
)

database_query_latency = Histogram(
    'chatbot_database_query_latency_seconds',
    'Database query latency',
    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5),
    registry=REGISTRY
)

errors_total = Counter(
    'chatbot_errors_total',
    'Total errors encountered',
    ['error_type'],
    registry=REGISTRY
)

active_sessions = Gauge(
    'chatbot_active_sessions',
    'Number of active sessions',
    registry=REGISTRY
)

redis_connection_errors = Counter(
    'chatbot_redis_connection_errors_total',
    'Total Redis connection errors',
    registry=REGISTRY
)

openai_rate_limit_errors = Counter(
    'chatbot_openai_rate_limit_errors_total',
    'Total OpenAI rate limit errors',
    registry=REGISTRY
)


class MetricsService:
    """Service for recording metrics"""

    @staticmethod
    def record_query(endpoint: str, status: str, duration: float):
        """Record query metrics

        Args:
            endpoint: API endpoint (e.g., 'query', 'selection')
            status: Response status ('success', 'error', 'rate_limited')
            duration: Query duration in seconds
        """
        query_latency.observe(duration)
        query_count.labels(endpoint=endpoint, status=status).inc()

    @staticmethod
    def record_cache_hit(cache_type: str):
        """Record cache hit

        Args:
            cache_type: Type of cache ('query' or 'embedding')
        """
        cache_hits.labels(cache_type=cache_type).inc()

    @staticmethod
    def record_cache_miss(cache_type: str):
        """Record cache miss

        Args:
            cache_type: Type of cache ('query' or 'embedding')
        """
        cache_misses.labels(cache_type=cache_type).inc()

    @staticmethod
    def record_openai_call(operation: str):
        """Record OpenAI API call

        Args:
            operation: Operation type ('chat_completion' or 'embedding')
        """
        openai_api_calls.labels(operation=operation).inc()

    @staticmethod
    def record_qdrant_search(duration: float):
        """Record Qdrant search

        Args:
            duration: Search duration in seconds
        """
        qdrant_searches.inc()
        qdrant_search_latency.observe(duration)

    @staticmethod
    def record_rate_limit_hit(session_id: str):
        """Record rate limit hit

        Args:
            session_id: Session ID that hit the rate limit
        """
        rate_limit_hits.labels(session_id=session_id).inc()

    @staticmethod
    def record_database_query(duration: float):
        """Record database query

        Args:
            duration: Query duration in seconds
        """
        database_query_latency.observe(duration)

    @staticmethod
    def record_error(error_type: str):
        """Record error

        Args:
            error_type: Type of error (e.g., 'openai_error', 'qdrant_error')
        """
        errors_total.labels(error_type=error_type).inc()

    @staticmethod
    def set_active_sessions(count: int):
        """Set number of active sessions

        Args:
            count: Number of active sessions
        """
        active_sessions.set(count)

    @staticmethod
    def record_redis_connection_error():
        """Record Redis connection error"""
        redis_connection_errors.inc()

    @staticmethod
    def record_openai_rate_limit_error():
        """Record OpenAI rate limit error"""
        openai_rate_limit_errors.inc()


def track_query_time(endpoint: str):
    """Decorator to track query execution time

    Usage:
        @track_query_time("query")
        async def query_endpoint(...):
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                MetricsService.record_query(endpoint, "success", duration)
                return result
            except Exception as e:
                duration = time.time() - start_time
                error_type = type(e).__name__
                MetricsService.record_query(endpoint, "error", duration)
                MetricsService.record_error(error_type)
                raise
        return wrapper
    return decorator


def get_metrics_summary() -> dict:
    """Get summary of current metrics

    Returns:
        Dictionary with metric summaries
    """
    return {
        "query_latency_histogram": {
            "buckets": [0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
            "help": "Query processing latency distribution"
        },
        "cache_hit_rate": {
            "help": "Percentage of requests served from cache"
        },
        "active_sessions": {
            "help": "Number of currently active sessions"
        },
        "error_rate": {
            "help": "Percentage of requests resulting in errors"
        }
    }
