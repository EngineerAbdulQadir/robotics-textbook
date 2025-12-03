"""Pytest configuration and shared fixtures for RAG chatbot tests."""

import pytest
from unittest.mock import MagicMock, AsyncMock
from typing import Generator


@pytest.fixture
def mock_qdrant_client():
    """Mock Qdrant client for vector search tests."""
    client = MagicMock()

    # Mock search response
    client.search.return_value = [
        MagicMock(
            id=1,
            score=0.95,
            payload={
                "chapter": "Module 1: ROS 2 Basics",
                "section": "Nodes and Topics",
                "content": "ROS 2 nodes communicate via topics using a publisher-subscriber pattern."
            }
        ),
        MagicMock(
            id=2,
            score=0.87,
            payload={
                "chapter": "Module 1: ROS 2 Basics",
                "section": "Services",
                "content": "Services provide request-reply communication between nodes."
            }
        )
    ]

    return client


@pytest.fixture
def mock_gemini_client():
    """Mock Gemini LLM client for response generation tests."""
    client = AsyncMock()

    # Mock generation response
    client.generate_content.return_value = MagicMock(
        text="ROS 2 nodes communicate through a publish-subscribe mechanism called topics. "
             "Publishers send messages to a topic, and subscribers receive those messages. "
             "This decouples nodes from each other, allowing flexible distributed communication."
    )

    return client


@pytest.fixture
def mock_neon_connection():
    """Mock Neon PostgreSQL connection pool."""
    pool = AsyncMock()

    # Mock acquire connection
    mock_conn = AsyncMock()
    pool.acquire.return_value.__aenter__.return_value = mock_conn

    return pool


@pytest.fixture
def mock_session():
    """Mock user session data."""
    return {
        "session_id": "test-session-123",
        "anonymous_browser_id": "browser-456",
        "created_at": "2025-11-30T10:00:00Z",
        "conversation_ids": ["conv-1", "conv-2"],
        "expires_at": "2025-12-30T10:00:00Z"
    }


@pytest.fixture
def mock_message():
    """Mock chat message."""
    return {
        "id": "msg-1",
        "conversation_id": "conv-1",
        "role": "user",
        "content": "How do ROS 2 nodes communicate?",
        "timestamp": "2025-11-30T10:05:00Z",
        "source_references": []
    }


@pytest.fixture
def mock_response():
    """Mock chatbot response."""
    return {
        "answer": "ROS 2 nodes communicate via topics using a publisher-subscriber pattern.",
        "sources": [
            {
                "chapter": "Module 1: ROS 2 Basics",
                "section": "Nodes and Topics",
                "content_excerpt": "ROS 2 nodes communicate via topics...",
                "link": "/docs/module-1/chapter-1#nodes-and-topics"
            }
        ],
        "session_id": "test-session-123",
        "message_id": "msg-1"
    }


@pytest.fixture
def mock_embedding():
    """Mock text embedding."""
    return [0.1, 0.2, 0.3] * 100  # 300-dimensional embedding


@pytest.fixture(scope="session")
def anyio_backend():
    """Configure anyio backend for async tests."""
    return "asyncio"
