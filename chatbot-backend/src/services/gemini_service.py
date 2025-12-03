"""Google Gemini LLM service for answer generation."""

import google.generativeai as genai
import logging
from typing import Optional

from ..config import settings
from ..utils.errors import GeminiException

logger = logging.getLogger(__name__)


class GeminiService:
    """Service for Google Gemini LLM operations."""

    def __init__(self):
        """Initialize Gemini client."""
        try:
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel(settings.gemini_model)
            logger.info(f"✓ Initialized Gemini model: {settings.gemini_model}")
        except Exception as e:
            logger.error(f"✗ Failed to initialize Gemini: {e}")
            raise GeminiException(f"Gemini initialization failed: {e}")

    async def generate_answer(
        self,
        question: str,
        context: str,
        max_tokens: int = 500
    ) -> str:
        """Generate answer using RAG prompt with context."""
        try:
            # Build RAG prompt - strict constraint to use only provided context
            rag_prompt = f"""You are an AI assistant helping readers understand a robotics textbook.

IMPORTANT: You MUST answer using ONLY the provided context. Do not use any knowledge outside the provided text.
If the information is not in the context, say "I don't find this information in the textbook."

Context from textbook:
{context}

User Question:
{question}

Answer (using ONLY the provided context):"""

            response = self.model.generate_content(rag_prompt)
            answer = response.text

            logger.info(f"✓ Generated answer via Gemini (tokens: {len(answer.split())})")
            return answer

        except Exception as e:
            logger.error(f"✗ Gemini generation failed: {e}")
            raise GeminiException(f"Answer generation failed: {e}")

    async def extract_key_points(
        self,
        text: str,
        num_points: int = 3
    ) -> list:
        """Extract key points from text."""
        try:
            prompt = f"""Extract {num_points} key points from the following text:

{text}

Key points (as a list):"""

            response = self.model.generate_content(prompt)
            # Simple parsing - would need more sophisticated approach in production
            points = response.text.split('\n')
            points = [p.strip() for p in points if p.strip()][:num_points]

            logger.info(f"✓ Extracted {len(points)} key points")
            return points

        except Exception as e:
            logger.error(f"✗ Key point extraction failed: {e}")
            return []

    async def health_check(self) -> bool:
        """Check Gemini API health by making a test request."""
        try:
            test_response = self.model.generate_content("Say 'ok'")
            logger.info("✓ Gemini health check passed")
            return True
        except Exception as e:
            logger.error(f"✗ Gemini health check failed: {e}")
            return False


# Global instance
_gemini_service = None


def get_gemini_service() -> GeminiService:
    """Get or create Gemini service instance."""
    global _gemini_service
    if _gemini_service is None:
        _gemini_service = GeminiService()
    return _gemini_service
