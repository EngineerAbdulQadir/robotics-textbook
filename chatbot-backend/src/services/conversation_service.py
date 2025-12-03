"""Conversation service for managing chat conversations."""

import logging
from datetime import datetime, timedelta
from uuid import UUID, uuid4
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.conversation import Conversation
from ..config import settings

logger = logging.getLogger(__name__)


class ConversationService:
    """Service for managing conversations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_create_conversation(
        self,
        session_id: UUID,
        page_context: Optional[str] = None
    ) -> Conversation:
        """
        Get existing conversation for session or create a new one.
        
        Args:
            session_id: User session UUID
            page_context: Optional page context (chapter, section, etc.)
            
        Returns:
            Conversation object
        """
        # Try to find existing conversation for this session
        stmt = select(Conversation).where(
            Conversation.user_session_id == session_id,
            Conversation.expires_at > datetime.utcnow()
        ).order_by(Conversation.created_at.desc())
        
        result = await self.db.execute(stmt)
        conversation = result.scalar_one_or_none()
        
        if conversation:
            # Update page context if provided
            if page_context and conversation.page_context != page_context:
                conversation.page_context = page_context
                conversation.updated_at = datetime.utcnow()
            logger.info(f"Found existing conversation {conversation.id} for session {session_id}")
            return conversation
        
        # Create new conversation
        conversation = Conversation(
            id=uuid4(),
            user_session_id=session_id,
            page_context=page_context,
            expires_at=datetime.utcnow() + timedelta(days=settings.session_expiry_days),
        )
        self.db.add(conversation)
        await self.db.flush()
        logger.info(f"Created new conversation {conversation.id} for session {session_id}")
        return conversation

    async def get_conversation(self, conversation_id: UUID) -> Optional[Conversation]:
        """Get conversation by ID."""
        stmt = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.expires_at > datetime.utcnow()
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_conversations_by_session(self, session_id: UUID) -> list[Conversation]:
        """Get all conversations for a session."""
        stmt = select(Conversation).where(
            Conversation.user_session_id == session_id,
            Conversation.expires_at > datetime.utcnow()
        ).order_by(Conversation.created_at.desc())
        
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
