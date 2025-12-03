"""OpenAI integration service for chat and embeddings"""

from openai import OpenAI, AsyncOpenAI
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class OpenAIService:
    """Service for OpenAI API interactions"""

    def __init__(self, api_key: str, model: str = "gpt-4", embedding_model: str = "text-embedding-3-small", cache_service: Optional['CacheService'] = None):
        """Initialize OpenAI client

        Args:
            api_key: OpenAI API key
            model: Chat model (default: gpt-4)
            embedding_model: Embedding model (default: text-embedding-3-small)
            cache_service: Optional cache service for embeddings (Redis)
        """
        self.api_key = api_key
        self.model = model
        self.embedding_model = embedding_model
        self.cache_service = cache_service
        self.client = OpenAI(api_key=api_key)
        self.async_client = AsyncOpenAI(api_key=api_key)

    async def chat_completion(
        self,
        messages: list[dict],
        system_prompt: str = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """Generate chat completion from OpenAI

        Args:
            messages: List of message dicts with 'role' and 'content'
            system_prompt: System prompt to prepend
            temperature: Temperature for response (0-2)
            max_tokens: Max tokens in response

        Returns:
            Assistant response text
        """
        try:
            # Prepare messages with system prompt
            if system_prompt:
                full_messages = [{"role": "system", "content": system_prompt}] + messages
            else:
                full_messages = messages

            response = await self.async_client.chat.completions.create(
                model=self.model,
                messages=full_messages,
                temperature=temperature,
                max_tokens=max_tokens
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise

    async def embed_text(self, text: str) -> list[float]:
        """Generate embedding for text with optional caching

        Args:
            text: Text to embed

        Returns:
            Embedding vector (list of floats)
        """
        try:
            # Check cache first if cache service is available
            if self.cache_service:
                cached_embedding = await self.cache_service.get_embedding_cache(text)
                if cached_embedding:
                    logger.debug(f"Cache hit for embedding of text: {text[:50]}...")
                    return cached_embedding

            response = await self.async_client.embeddings.create(
                model=self.embedding_model,
                input=text
            )

            embedding = response.data[0].embedding

            # Cache the embedding if cache service is available
            if self.cache_service:
                await self.cache_service.set_embedding_cache(text, embedding)

            return embedding

        except Exception as e:
            logger.error(f"OpenAI embedding error: {str(e)}")
            raise

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        try:
            response = await self.async_client.embeddings.create(
                model=self.embedding_model,
                input=texts
            )

            # Sort by index to maintain order
            embeddings = sorted(response.data, key=lambda x: x.index)
            return [item.embedding for item in embeddings]

        except Exception as e:
            logger.error(f"OpenAI batch embedding error: {str(e)}")
            raise

    def sync_chat_completion(
        self,
        messages: list[dict],
        system_prompt: str = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """Synchronous chat completion (for testing)

        Args:
            messages: List of message dicts
            system_prompt: System prompt to prepend
            temperature: Temperature for response
            max_tokens: Max tokens in response

        Returns:
            Assistant response text
        """
        try:
            if system_prompt:
                full_messages = [{"role": "system", "content": system_prompt}] + messages
            else:
                full_messages = messages

            response = self.client.chat.completions.create(
                model=self.model,
                messages=full_messages,
                temperature=temperature,
                max_tokens=max_tokens
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"OpenAI sync API error: {str(e)}")
            raise

    def sync_embed_text(self, text: str) -> list[float]:
        """Synchronous embedding generation (for testing)

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        try:
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=text
            )

            return response.data[0].embedding

        except Exception as e:
            logger.error(f"OpenAI sync embedding error: {str(e)}")
            raise
