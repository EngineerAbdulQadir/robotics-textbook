"""Analytics and metrics tracking service."""

import logging
from typing import Optional
from datetime import datetime, timedelta
from enum import Enum
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

logger = logging.getLogger(__name__)


class EventType(str, Enum):
    """Types of events to track."""

    QUERY = "query"
    SELECTION = "selection"
    ERROR = "error"
    SESSION_START = "session_start"
    SESSION_END = "session_end"
    CACHE_HIT = "cache_hit"
    CACHE_MISS = "cache_miss"


class AnalyticsService:
    """Service for tracking analytics and metrics."""

    def __init__(self, db: Optional[AsyncSession] = None):
        """Initialize analytics service."""
        self.db = db
        self.events = []
        self.session_metrics = {}

    async def track_event(
        self,
        event_type: EventType,
        session_id: str,
        data: Optional[dict] = None,
        duration_ms: Optional[float] = None,
    ) -> None:
        """
        Track an analytics event.

        Args:
            event_type: Type of event
            session_id: Session ID
            data: Additional event data
            duration_ms: Duration in milliseconds
        """
        try:
            event = {
                "type": event_type.value,
                "session_id": session_id,
                "timestamp": datetime.utcnow(),
                "data": data or {},
                "duration_ms": duration_ms,
            }

            self.events.append(event)
            logger.debug(f"📊 Tracked event: {event_type.value}")

            # Store in database if available
            if self.db:
                await self._store_event(event)

        except Exception as e:
            logger.warning(f"Event tracking error: {e}")

    async def _store_event(self, event: dict) -> None:
        """Store event in database."""
        try:
            # In production, would insert into events table
            logger.debug(f"Stored event in database: {event['type']}")
        except Exception as e:
            logger.warning(f"Database storage error: {e}")

    async def get_session_metrics(self, session_id: str) -> dict:
        """Get metrics for a session."""
        session_events = [
            e for e in self.events
            if e["session_id"] == session_id
        ]

        queries = sum(1 for e in session_events if e["type"] == "query")
        selections = sum(1 for e in session_events if e["type"] == "selection")
        errors = sum(1 for e in session_events if e["type"] == "error")
        cache_hits = sum(1 for e in session_events if e["type"] == "cache_hit")

        total_duration = sum(
            e["duration_ms"] for e in session_events
            if e["duration_ms"]
        ) or 0

        return {
            "session_id": session_id,
            "total_queries": queries,
            "total_selections": selections,
            "total_errors": errors,
            "cache_hit_rate": (
                cache_hits / max(queries + cache_hits, 1) * 100
                if queries + cache_hits > 0
                else 0
            ),
            "average_response_time_ms": (
                total_duration / (queries + selections)
                if queries + selections > 0
                else 0
            ),
            "event_count": len(session_events),
        }

    async def get_global_metrics(self) -> dict:
        """Get global metrics across all sessions."""
        if not self.events:
            return {
                "total_queries": 0,
                "total_sessions": 0,
                "average_confidence": 0.0,
            }

        queries = sum(1 for e in self.events if e["type"] == "query")
        selections = sum(1 for e in self.events if e["type"] == "selection")
        errors = sum(1 for e in self.events if e["type"] == "error")
        sessions = len(set(e["session_id"] for e in self.events))

        total_duration = sum(
            e["duration_ms"] for e in self.events
            if e["duration_ms"]
        ) or 0

        return {
            "total_queries": queries,
            "total_selections": selections,
            "total_errors": errors,
            "total_sessions": sessions,
            "average_response_time_ms": (
                total_duration / max(queries + selections, 1)
            ),
            "error_rate": (
                errors / max(queries + selections, 1) * 100
                if queries + selections > 0
                else 0
            ),
        }

    async def get_popular_queries(self, limit: int = 10) -> list:
        """Get most frequently asked questions."""
        query_events = [
            e for e in self.events
            if e["type"] == "query"
        ]

        query_counts = {}
        for event in query_events:
            question = event.get("data", {}).get("question", "")
            if question:
                query_counts[question] = query_counts.get(question, 0) + 1

        # Sort by count and return top N
        popular = sorted(
            query_counts.items(),
            key=lambda x: x[1],
            reverse=True,
        )[:limit]

        return [
            {
                "question": q,
                "count": count,
                "percentage": (count / len(query_events) * 100)
                if query_events
                else 0,
            }
            for q, count in popular
        ]

    async def get_performance_metrics(self) -> dict:
        """Get performance metrics."""
        if not self.events:
            return {"p50": 0, "p95": 0, "p99": 0}

        durations = sorted([
            e["duration_ms"] for e in self.events
            if e["duration_ms"]
        ])

        if not durations:
            return {"p50": 0, "p95": 0, "p99": 0}

        return {
            "min_ms": min(durations),
            "max_ms": max(durations),
            "p50_ms": durations[int(len(durations) * 0.5)],
            "p95_ms": durations[int(len(durations) * 0.95)],
            "p99_ms": durations[int(len(durations) * 0.99)],
            "average_ms": sum(durations) / len(durations),
        }

    async def clear_old_events(self, days: int = 7) -> int:
        """Clear events older than specified days."""
        cutoff = datetime.utcnow() - timedelta(days=days)
        old_events = [
            e for e in self.events
            if e["timestamp"] < cutoff
        ]

        count = len(old_events)
        self.events = [
            e for e in self.events
            if e["timestamp"] >= cutoff
        ]

        logger.info(f"✓ Cleared {count} old events")
        return count


# Global instance
_analytics_service = None


def get_analytics_service(db: Optional[AsyncSession] = None) -> AnalyticsService:
    """Get or create analytics service instance."""
    global _analytics_service
    if _analytics_service is None:
        _analytics_service = AnalyticsService(db)
    return _analytics_service
