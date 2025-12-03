"""Conversation model - groups related messages."""

from datetime import datetime, timedelta
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from . import Base


class Conversation(Base):
    """Conversation - groups related messages from a user session."""

    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_session_id = Column(UUID(as_uuid=True), ForeignKey("user_sessions.session_id", ondelete="CASCADE"), nullable=False)
    page_context = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)

    # Relationships
    messages = relationship("Message", cascade="all, delete-orphan", back_populates="conversation")

    __table_args__ = (
        Index('ix_conversations_user_session_id', 'user_session_id'),
        Index('ix_conversations_created_at', 'created_at'),
        Index('ix_conversations_expires_at', 'expires_at'),
    )

    def __repr__(self):
        return f"<Conversation(id={self.id}, user_session_id={self.user_session_id})>"

    @staticmethod
    def create(user_session_id: str, page_context: str = None, ttl_days: int = 30):
        """Create new conversation with TTL."""
        return Conversation(
            id=uuid4(),
            user_session_id=user_session_id,
            page_context=page_context,
            expires_at=datetime.utcnow() + timedelta(days=ttl_days),
        )
