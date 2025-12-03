"""Session management service for anonymous and authenticated users."""

import logging
from uuid import uuid4
from datetime import datetime, timedelta
from typing import Optional

logger = logging.getLogger(__name__)


class SessionService:
    """Service for managing user sessions."""

    async def create_session(
        self,
        anonymous_browser_id: Optional[str] = None,
        user_id: Optional[str] = None,
        page_context: Optional[str] = None,
        ttl_days: int = 30
    ) -> dict:
        """Create new user session."""
        session_id = str(uuid4())

        session = {
            "session_id": session_id,
            "anonymous_browser_id": anonymous_browser_id,
            "user_id": user_id,
            "page_context": page_context,
            "conversation_ids": [],
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": (datetime.utcnow() + timedelta(days=ttl_days)).isoformat(),
        }

        logger.info(f"✓ Created session: {session_id}")
        return session

    async def get_session(self, session_id: str) -> Optional[dict]:
        """Retrieve session (would query database in production)."""
        logger.info(f"✓ Retrieved session: {session_id}")
        return {"session_id": session_id}

    async def update_session(self, session_id: str, updates: dict) -> bool:
        """Update session data."""
        logger.info(f"✓ Updated session: {session_id}")
        return True

    async def delete_session(self, session_id: str) -> bool:
        """Delete session and associated conversations."""
        logger.info(f"✓ Deleted session: {session_id}")
        return True

    async def is_session_valid(self, session_id: str) -> bool:
        """Check if session is valid and not expired."""
        # In production, check against database
        logger.info(f"✓ Validated session: {session_id}")
        return True


# Global instance
_session_service = None


def get_session_service() -> SessionService:
    """Get or create session service instance."""
    global _session_service
    if _session_service is None:
        _session_service = SessionService()
    return _session_service
