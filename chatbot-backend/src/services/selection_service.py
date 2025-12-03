"""Selection-based Q&A service for highlighted textbook content."""

import logging
from typing import List, Tuple
from datetime import datetime, timedelta

from ..models.schemas import CitationSchema
from ..models.citation import Citation
from ..config import settings
from .qdrant_service import get_qdrant_service
from .gemini_service import get_gemini_service
from .embedding_service import get_embedding_service
from ..utils.errors import RAGException

logger = logging.getLogger(__name__)


class SelectionService:
    """Service for Q&A on selected text passages."""

    def __init__(self):
        """Initialize selection service with dependencies."""
        self.qdrant_service = get_qdrant_service()
        self.gemini_service = get_gemini_service()
        self.embedding_service = get_embedding_service()

    async def process_selection_question(
        self,
        selected_text: str,
        question: str,
        chapter: str,
        section: str = "",
    ) -> Tuple[str, List[Citation], float]:
        """
        Process question about selected text.

        Args:
            selected_text: User-selected text from textbook
            question: User question about selected text
            chapter: Chapter containing the selection
            section: Optional section name

        Returns:
            Tuple of (answer, citations, confidence)

        Raises:
            RAGException: For service errors
        """
        try:
            logger.info(f"🔍 Processing selection question for chapter '{chapter}'")

            # Step 1: Embed the question
            question_embedding = await self.embedding_service.embed_text(question)
            logger.info(f"✓ Generated question embedding ({len(question_embedding)} dims)")

            # Step 2: Search for related content in same chapter/section
            related_results = await self.qdrant_service.search(
                query_vector=question_embedding,
                top_k=3,  # Fewer results for selection-based context
                score_threshold=0.4,  # Lower threshold to find related content
            )

            # Filter results to same chapter if possible
            same_chapter_results = [
                r for r in related_results
                if r.get("chapter") == chapter
            ]
            if same_chapter_results:
                related_results = same_chapter_results[:3]

            logger.info(f"✓ Retrieved {len(related_results)} related passages")

            # Step 3: Build context with selected text as primary source
            context = self._build_selection_context(
                selected_text,
                related_results,
                chapter,
                section,
            )

            # Step 4: Generate answer with selection-specific prompts
            answer = await self._generate_selection_answer(
                question=question,
                selected_text=selected_text,
                context=context,
                chapter=chapter,
                section=section,
            )
            logger.info(f"✓ Generated answer for selection question")

            # Step 5: Create citations (primary citation is the selection)
            citations = self._create_selection_citations(
                selected_text=selected_text,
                chapter=chapter,
                section=section,
                related_results=related_results,
            )
            confidence = self._calculate_confidence(citations)

            logger.info(f"✓ Created {len(citations)} citations, confidence: {confidence:.2f}")
            return answer, citations, confidence

        except Exception as e:
            logger.error(f"❌ Selection processing failed: {e}")
            raise RAGException(f"Selection Q&A failed: {e}")

    async def extract_selection_context(
        self,
        selected_text: str,
    ) -> dict:
        """
        Extract and analyze selection for contextual information.

        Args:
            selected_text: Selected text passage

        Returns:
            Dictionary with extracted context (key_terms, length, etc.)
        """
        try:
            logger.info("Analyzing selected text context...")

            # Extract key terms from selection (simple word frequency)
            words = selected_text.lower().split()
            key_terms = [w for w in words if len(w) > 4][:5]

            return {
                "text_length": len(selected_text),
                "word_count": len(words),
                "key_terms": key_terms,
            }
        except Exception as e:
            logger.warning(f"Context extraction error: {e}")
            return {"text_length": len(selected_text), "word_count": len(selected_text.split())}

    def _build_selection_context(
        self,
        selected_text: str,
        related_results: List[dict],
        chapter: str,
        section: str = "",
    ) -> str:
        """Build context with selected text as primary source."""
        section_str = f', Section "{section}"' if section else ""
        context_parts = [
            f"SELECTED TEXT (from Chapter '{chapter}'{section_str}):",
            selected_text,
            "\n" + "=" * 50 + "\n",
        ]

        if related_results:
            context_parts.append("RELATED PASSAGES FOR CONTEXT:")
            for result in related_results:
                ch = result.get("chapter", "")
                sec = result.get("section", "")
                content = result.get("content", "")
                context_parts.append(
                    f"\nFrom {ch}, {sec}:\n{content}"
                )

        return "\n".join(context_parts)

    async def _generate_selection_answer(
        self,
        question: str,
        selected_text: str,
        context: str,
        chapter: str,
        section: str,
    ) -> str:
        """Generate answer with selection-specific RAG prompt."""
        # Selection-specific prompt emphasizes the selected text
        selection_prompt = f"""You are an AI assistant helping readers understand a robotics textbook.

The user has selected a specific passage from the textbook and has a question about it.

IMPORTANT:
1. Focus your answer on the selected text
2. Use related passages only for clarification
3. Answer must be grounded in the textbook content
4. If the question cannot be answered from the selected text, say "This question goes beyond the selected passage"

QUESTION FROM USER: {question}

{context}

ANSWER (focused on the selected text):"""

        # Use Gemini service with custom prompt
        response = await self.gemini_service.generate_answer(
            question=question,
            context=context,
            max_tokens=300,  # Shorter for selection-focused answers
        )

        return response

    def _create_selection_citations(
        self,
        selected_text: str,
        chapter: str,
        section: str,
        related_results: List[dict],
    ) -> List[Citation]:
        """Create citations with selected text as primary source."""
        citations = []

        # Primary citation: the selected text itself
        primary_citation = Citation(
            id=None,
            message_id=None,
            chapter=chapter,
            section=section,
            content_excerpt=selected_text[:500],
            link=None,
            confidence_score=1.0,  # High confidence for directly selected text
            expires_at=datetime.utcnow() + timedelta(days=settings.session_expiry_days),
        )
        citations.append(primary_citation)

        # Secondary citations from related results
        for result in related_results:
            citation = Citation(
                id=None,
                message_id=None,
                chapter=result.get("chapter", ""),
                section=result.get("section", ""),
                content_excerpt=result.get("content", "")[:500],
                link=result.get("link"),
                confidence_score=float(result.get("score", 0.5)),
                expires_at=datetime.utcnow() + timedelta(days=settings.session_expiry_days),
            )
            citations.append(citation)

        return citations

    def _calculate_confidence(self, citations: List[Citation]) -> float:
        """Calculate confidence with primary citation weighted higher."""
        if not citations:
            return 0.0

        # Primary citation (selected text) has weight 1.0
        # Secondary citations weighted by their scores
        if len(citations) == 1:
            return citations[0].confidence_score

        primary_score = citations[0].confidence_score
        secondary_scores = [c.confidence_score for c in citations[1:]]
        secondary_avg = sum(secondary_scores) / len(secondary_scores) if secondary_scores else 0.0

        # Weight: 60% primary, 40% secondary
        confidence = (0.6 * primary_score) + (0.4 * secondary_avg)
        return min(confidence, 1.0)


# Global instance
_selection_service = None


def get_selection_service() -> SelectionService:
    """Get or create selection service instance."""
    global _selection_service
    if _selection_service is None:
        _selection_service = SelectionService()
    return _selection_service
