"""Text embedding service for RAG retrieval."""

import logging
from typing import List
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating text embeddings."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize embedding model."""
        try:
            self.model = SentenceTransformer(model_name)
            self.model_name = model_name
            logger.info(f"✓ Loaded embedding model: {model_name}")
        except Exception as e:
            logger.error(f"✗ Failed to load embedding model: {e}")
            raise

    async def embed_text(self, text: str) -> List[float]:
        """Generate embedding for text."""
        try:
            embedding = self.model.encode(text, convert_to_tensor=False)
            logger.info(f"✓ Generated embedding for text ({len(embedding)} dimensions)")
            return embedding.tolist()

        except Exception as e:
            logger.error(f"✗ Embedding generation failed: {e}")
            raise

    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        try:
            embeddings = self.model.encode(texts, convert_to_tensor=False)
            logger.info(f"✓ Generated embeddings for {len(texts)} texts")
            return [emb.tolist() for emb in embeddings]

        except Exception as e:
            logger.error(f"✗ Batch embedding failed: {e}")
            raise


# Global instance
_embedding_service = None


def get_embedding_service() -> EmbeddingService:
    """Get or create embedding service instance."""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service
