"""Custom exception classes for RAG chatbot."""


class RAGException(Exception):
    """Base exception for RAG chatbot."""

    pass


class DatabaseException(RAGException):
    """Database operation error."""

    pass


class QdrantException(RAGException):
    """Qdrant vector database error."""

    pass


class GeminiException(RAGException):
    """Gemini LLM API error."""

    pass


class RateLimitException(RAGException):
    """Rate limit exceeded."""

    pass


class HallucationDetectedException(RAGException):
    """Potential hallucination detected in response."""

    pass


class InvalidSessionException(RAGException):
    """Invalid or expired session."""

    pass


class NotFoundError(RAGException):
    """Resource not found."""

    pass
