"""Create initial schema with 6 core tables.

Revision ID: 001_initial
Revises:
Create Date: 2025-11-30 12:00:00.000000

Tables:
- users (optional, for future authentication)
- user_sessions (anonymous + authenticated tracking)
- conversations (message groupings)
- messages (user questions + AI responses)
- textbook_content (indexed chunks with vectors)
- citations (answer sources)
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create initial database schema."""

    # Create user_sessions table
    op.create_table(
        'user_sessions',
        sa.Column('session_id', postgresql.UUID(as_uuid=True), nullable=False, primary_key=True),
        sa.Column('anonymous_browser_id', sa.String(255), nullable=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('page_context', sa.String(500), nullable=True),
        sa.Column('conversation_ids', postgresql.JSON(), nullable=True, server_default='[]'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_user_sessions_session_id', 'user_sessions', ['session_id'])
    op.create_index('ix_user_sessions_user_id', 'user_sessions', ['user_id'])
    op.create_index('ix_user_sessions_expires_at', 'user_sessions', ['expires_at'])

    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, primary_key=True),
        sa.Column('user_session_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('page_context', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_session_id'], ['user_sessions.session_id'], ondelete='CASCADE'),
    )
    op.create_index('ix_conversations_user_session_id', 'conversations', ['user_session_id'])
    op.create_index('ix_conversations_created_at', 'conversations', ['created_at'])
    op.create_index('ix_conversations_expires_at', 'conversations', ['expires_at'])

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, primary_key=True),
        sa.Column('conversation_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('role', sa.Enum('user', 'assistant', name='message_role'), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('source_references', postgresql.JSON(), nullable=True, server_default='[]'),
        sa.Column('timestamp', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_messages_conversation_id', 'messages', ['conversation_id'])
    op.create_index('ix_messages_timestamp', 'messages', ['timestamp'])
    op.create_index('ix_messages_expires_at', 'messages', ['expires_at'])

    # Create textbook_content table
    op.create_table(
        'textbook_content',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, primary_key=True),
        sa.Column('chapter', sa.String(500), nullable=False),
        sa.Column('section', sa.String(500), nullable=False),
        sa.Column('content_text', sa.Text(), nullable=False),
        sa.Column('vector_embedding_id', sa.String(255), nullable=True),
        sa.Column('metadata', postgresql.JSON(), nullable=True, server_default='{}'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index('ix_textbook_content_chapter', 'textbook_content', ['chapter'])
    op.create_index('ix_textbook_content_section', 'textbook_content', ['section'])

    # Create citations table
    op.create_table(
        'citations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, primary_key=True),
        sa.Column('message_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('chapter', sa.String(500), nullable=False),
        sa.Column('section', sa.String(500), nullable=False),
        sa.Column('content_excerpt', sa.Text(), nullable=False),
        sa.Column('link', sa.String(1000), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['message_id'], ['messages.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_citations_message_id', 'citations', ['message_id'])
    op.create_index('ix_citations_expires_at', 'citations', ['expires_at'])


def downgrade() -> None:
    """Drop all tables."""
    op.drop_table('citations')
    op.drop_table('textbook_content')
    op.drop_table('messages')
    op.drop_table('conversations')
    op.drop_table('user_sessions')
