"""Qdrant vector database service"""

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import PointStruct
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class QdrantService:
    """Service for Qdrant vector database operations"""

    def __init__(self, url: str, api_key: str, collection_name: str = "textbook_content"):
        self.url = url
        self.api_key = api_key
        self.collection_name = collection_name
        self.client = AsyncQdrantClient(url=url, api_key=api_key)

    async def health_check(self) -> bool:
        """Check if Qdrant is healthy"""
        try:
            await self.client.api_key_managed
            return True
        except Exception as e:
            logger.error(f"Qdrant health check failed: {str(e)}")
            return False

    async def search(
        self,
        vector: List[float],
        limit: int = 5,
        score_threshold: float = 0.0
    ) -> List[dict]:
        """Search for similar vectors in collection"""
        try:
            logger.info(f"🔍 Searching Qdrant collection: {self.collection_name}")
            
            # Use query_points for newer qdrant-client versions
            # Remove score_threshold to get all results
            results = await self.client.query_points(
                collection_name=self.collection_name,
                query=vector,
                limit=limit
            )

            formatted_results = []
            for point in results.points:
                logger.info(f"  Found: score={point.score:.3f}, content={str(point.payload.get('content', ''))[:50]}...")
                formatted_results.append({
                    "id": point.id,
                    "score": point.score,
                    "payload": point.payload if hasattr(point, 'payload') else {}
                })

            logger.info(f"✅ Qdrant returned {len(formatted_results)} results")
            return formatted_results

        except Exception as e:
            logger.error(f"❌ Qdrant search error: {str(e)}", exc_info=True)
            raise

    async def search_with_chapter_filter(
        self,
        vector: List[float],
        chapter: str,
        limit: int = 5,
        score_threshold: float = 0.3
    ) -> List[dict]:
        """Search with chapter filtering"""
        try:
            results = await self.client.query_points(
                collection_name=self.collection_name,
                query=vector,
                limit=limit,
                score_threshold=score_threshold
            )

            formatted_results = []
            for point in results.points:
                if point.payload.get("chapter") == chapter:
                    formatted_results.append({
                        "id": point.id,
                        "score": point.score,
                        "payload": point.payload
                    })
                if len(formatted_results) >= limit:
                    break

            return formatted_results

        except Exception as e:
            logger.error(f"Qdrant filtered search error: {str(e)}")
            return await self.search(vector, limit, score_threshold)

    async def get_collection_info(self) -> Optional[dict]:
        """Get collection information"""
        try:
            collection_info = await self.client.get_collection(self.collection_name)
            return {
                "name": self.collection_name,
                "vectors_count": getattr(collection_info, 'vectors_count', 0),
                "points_count": getattr(collection_info, 'points_count', 0)
            }
        except Exception as e:
            logger.error(f"Qdrant collection info error: {str(e)}")
            return None
