"""Citation model - links answers to source textbook content."""

from datetime import datetime, timedelta
from uuid import uuid4
from sqlalchemy import Column, String, Text, Float, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from . import Base


class Citation(Base):
    """Citation - links answer to source textbook content."""

    __tablename__ = "citations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    message_id = Column(UUID(as_uuid=True), ForeignKey("messages.id", ondelete="CASCADE"), nullable=False)
    chapter = Column(String(500), nullable=False)
    section = Column(String(500), nullable=False)
    content_excerpt = Column(Text(), nullable=False)
    link = Column(String(1000), nullable=True)
    confidence_score = Column(Float(), default=0.0)
    expires_at = Column(DateTime, nullable=False)

    # Relationships
    message = relationship("Message", back_populates="citations")

    __table_args__ = (
        Index('ix_citations_message_id', 'message_id'),
        Index('ix_citations_expires_at', 'expires_at'),
    )

    def __repr__(self):
        return f"<Citation(id={self.id}, chapter={self.chapter}, section={self.section})>"

    @staticmethod
    def create(message_id: str, chapter: str, section: str, excerpt: str, link: str = None, confidence: float = 0.0, ttl_days: int = 30):
        """Create citation for answer."""
        return Citation(
            id=uuid4(),
            message_id=message_id,
            chapter=chapter,
            section=section,
            content_excerpt=excerpt,
            link=link,
            confidence_score=confidence,
            expires_at=datetime.utcnow() + timedelta(days=ttl_days),
        )
