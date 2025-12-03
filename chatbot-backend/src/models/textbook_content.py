"""TextbookContent model - indexed textbook chunks for RAG retrieval."""

from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, Text, DateTime, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from . import Base


class TextbookContent(Base):
    """Textbook content chunk - indexed in Qdrant for semantic search."""

    __tablename__ = "textbook_content"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    chapter = Column(String(500), nullable=False)
    section = Column(String(500), nullable=False)
    content_text = Column(Text(), nullable=False)
    vector_embedding_id = Column(String(255), nullable=True)
    metadata = Column(JSON(), default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index('ix_textbook_content_chapter', 'chapter'),
        Index('ix_textbook_content_section', 'section'),
    )

    def __repr__(self):
        return f"<TextbookContent(id={self.id}, chapter={self.chapter})>"

    @staticmethod
    def create(chapter: str, section: str, content_text: str, metadata: dict = None):
        """Create textbook content chunk."""
        return TextbookContent(
            id=uuid4(),
            chapter=chapter,
            section=section,
            content_text=content_text,
            metadata=metadata or {"tokens": len(content_text.split()), "difficulty": "medium"},
        )
