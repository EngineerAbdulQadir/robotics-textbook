"""RAG (Retrieval-Augmented Generation) pipeline service"""

from .openai_service import OpenAIService
from .qdrant_service import QdrantService
from .cache_service import CacheService
import logging
from typing import Optional, List

logger = logging.getLogger(__name__)


class RAGService:
    """Main RAG service coordinating the pipeline"""

    def __init__(self, openai_service: OpenAIService, qdrant_service: QdrantService, cache_service: CacheService):
        self.openai = openai_service
        self.qdrant = qdrant_service
        self.cache = cache_service

    async def process_query(self, question: str, session_id: str, page_context: Optional[str] = None) -> dict:
        """Process a query through the RAG pipeline"""

        cached_result = await self.cache.get_query_cache(question, session_id)
        if cached_result:
            logger.info(f"Cache hit for question")
            return cached_result

        try:
            if not question or len(question) < 1 or len(question) > 500:
                raise ValueError("Question must be 1-500 characters")

            logger.info(f"🔍 Generating embedding for: {question[:50]}...")
            embedding = await self.openai.embed_text(question)
            logger.info(f"✅ Embedding generated, dimension: {len(embedding)}")
            
            # Use lower threshold to get more results
            logger.info(f"🔍 Searching Qdrant...")
            search_results = await self.qdrant.search(vector=embedding, limit=5, score_threshold=0.1)
            logger.info(f"✅ Found {len(search_results)} results")

            if not search_results:
                logger.warning("⚠️ No search results found")
                # Still try to answer using OpenAI without context
                system_prompt = "You are a helpful assistant for a ROS 2 and robotics textbook. Answer the question helpfully."
                messages = [{"role": "user", "content": question}]
                answer = await self.openai.chat_completion(messages=messages, system_prompt=system_prompt)
                return {"answer": answer, "sources": [], "confidence": 0.0}

            context = self._build_context(search_results, page_context)
            logger.info(f"📝 Built context with {len(context)} characters")
            
            system_prompt = """You are a helpful assistant for a Physical AI and Robotics textbook about ROS 2.
Answer the question based on the provided context. Be helpful and informative.
If the context doesn't contain relevant information, say so but still try to help."""
            
            messages = [{"role": "user", "content": f"Context from textbook:\n{context}\n\nQuestion: {question}"}]
            
            logger.info(f"🤖 Calling OpenAI for answer...")
            answer = await self.openai.chat_completion(messages=messages, system_prompt=system_prompt)
            logger.info(f"✅ Got answer: {answer[:100]}...")
            
            citations = self._extract_citations(answer, search_results)
            confidence = self._calculate_confidence(search_results)

            response = {"answer": answer, "sources": citations, "confidence": confidence, "session_id": session_id}
            await self.cache.set_query_cache(question, session_id, response)

            return response

        except Exception as e:
            logger.error(f"❌ RAG pipeline error: {str(e)}", exc_info=True)
            raise

    def _build_context(self, search_results: List[dict], page_context: Optional[str]) -> str:
        """Build context from search results"""
        parts = []
        if page_context:
            parts.append(f"Context: {page_context}")
        for i, result in enumerate(search_results, 1):
            payload = result.get("payload", {})
            parts.append(f"[{i}] {payload.get('content', '')[:300]}")
        return "\n".join(parts)

    def _extract_citations(self, answer: str, search_results: List[dict]) -> List[dict]:
        """Extract citations from answer and search results"""
        return [{"id": r.get("id"), "score": r.get("score", 0), "payload": r.get("payload", {})} for r in search_results]

    def _calculate_confidence(self, search_results: List[dict]) -> float:
        """Calculate overall confidence from search results"""
        if not search_results:
            return 0.0
        scores = [result.get("score", 0) for result in search_results]
        return sum(scores) / len(scores)
