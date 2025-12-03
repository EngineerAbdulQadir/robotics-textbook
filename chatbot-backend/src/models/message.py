"""Message model - represents chat messages (user questions or AI responses)."""

from datetime import datetime, timedelta
from enum import Enum
from uuid import uuid4
from sqlalchemy import Column, String, Text, Enum as SQLEnum, DateTime, ForeignKey, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from . import Base


class MessageRole(str, Enum):
    """Message role enum."""

    USER = "user"
    ASSISTANT = "assistant"


class Message(Base):
    """Chat message - user question or AI response."""

    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    role = Column(SQLEnum(MessageRole), nullable=False)
    content = Column(Text(), nullable=False)
    source_references = Column(JSON(), default=list)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    citations = relationship("Citation", cascade="all, delete-orphan", back_populates="message")

    __table_args__ = (
        Index('ix_messages_conversation_id', 'conversation_id'),
        Index('ix_messages_timestamp', 'timestamp'),
        Index('ix_messages_expires_at', 'expires_at'),
    )

    def __repr__(self):
        return f"<Message(id={self.id}, role={self.role}, conversation_id={self.conversation_id})>"

    @staticmethod
    def create_user_message(conversation_id: str, content: str, ttl_days: int = 30):
        """Create user message."""
        return Message(
            id=uuid4(),
            conversation_id=conversation_id,
            role=MessageRole.USER,
            content=content,
            source_references=[],
            expires_at=datetime.utcnow() + timedelta(days=ttl_days),
        )

    @staticmethod
    def create_assistant_message(conversation_id: str, content: str, source_references: list = None, ttl_days: int = 30):
        """Create assistant response message."""
        return Message(
            id=uuid4(),
            conversation_id=conversation_id,
            role=MessageRole.ASSISTANT,
            content=content,
            source_references=source_references or [],
            expires_at=datetime.utcnow() + timedelta(days=ttl_days),
        )
