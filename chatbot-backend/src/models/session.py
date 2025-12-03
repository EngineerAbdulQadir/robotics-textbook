"""UserSession model for tracking user sessions (anonymous + authenticated)."""

from datetime import datetime, timedelta
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from . import Base


class UserSession(Base):
    """User session - tracks browser session or authenticated user."""

    __tablename__ = "user_sessions"

    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    anonymous_browser_id = Column(String(255), nullable=True)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    page_context = Column(String(500), nullable=True)
    conversation_ids = Column(JSON(), default=list)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)

    __table_args__ = (
        Index('ix_user_sessions_session_id', 'session_id'),
        Index('ix_user_sessions_user_id', 'user_id'),
        Index('ix_user_sessions_expires_at', 'expires_at'),
    )

    def __repr__(self):
        return f"<UserSession(session_id={self.session_id}, user_id={self.user_id})>"

    @staticmethod
    def create(anonymous_browser_id: str = None, user_id: str = None, page_context: str = None, ttl_days: int = 30):
        """Create new session with TTL."""
        return UserSession(
            session_id=uuid4(),
            anonymous_browser_id=anonymous_browser_id,
            user_id=user_id,
            page_context=page_context,
            conversation_ids=[],
            expires_at=datetime.utcnow() + timedelta(days=ttl_days),
        )
