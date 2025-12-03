"""Redis cache service"""

import redis.asyncio as redis
import json
import hashlib
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


class CacheService:
    """Service for Redis caching operations"""

    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis: Optional[redis.Redis] = None

    async def initialize(self):
        """Initialize Redis connection"""
        try:
            self.redis = await redis.from_url(self.redis_url, decode_responses=True)
            await self.redis.ping()
            logger.info("Redis connected successfully")
        except Exception as e:
            logger.error(f"Redis connection failed: {str(e)}")
            self.redis = None

    async def close(self):
        """Close Redis connection"""
        if self.redis:
            await self.redis.close()

    async def health_check(self) -> bool:
        """Check if Redis is healthy"""
        try:
            if self.redis:
                await self.redis.ping()
                return True
        except Exception as e:
            logger.error(f"Redis health check failed: {str(e)}")
        return False

    def _generate_key(self, *args) -> str:
        """Generate cache key from arguments"""
        key_str = "|".join(str(arg) for arg in args)
        return hashlib.md5(key_str.encode()).hexdigest()

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.redis:
            return None
        try:
            value = await self.redis.get(key)
            if value:
                return json.loads(value)
        except Exception as e:
            logger.error(f"Cache get error: {str(e)}")
        return None

    async def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set value in cache with TTL"""
        if not self.redis:
            return False
        try:
            await self.redis.setex(key, ttl, json.dumps(value))
            return True
        except Exception as e:
            logger.error(f"Cache set error: {str(e)}")
            return False

    async def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if not self.redis:
            return False
        try:
            await self.redis.delete(key)
            return True
        except Exception as e:
            logger.error(f"Cache delete error: {str(e)}")
            return False

    async def get_query_cache(self, question: str, session_id: str) -> Optional[dict]:
        """Get cached query result (1 hour TTL)"""
        key = self._generate_key("query", question, session_id)
        return await self.get(key)

    async def set_query_cache(self, question: str, session_id: str, result: dict) -> bool:
        """Cache query result for 1 hour"""
        key = self._generate_key("query", question, session_id)
        return await self.set(key, result, ttl=3600)

    async def get_embedding_cache(self, text: str) -> Optional[list]:
        """Get cached embedding (24 hour TTL)"""
        key = self._generate_key("embedding", text)
        return await self.get(key)

    async def set_embedding_cache(self, text: str, embedding: list) -> bool:
        """Cache embedding for 24 hours"""
        key = self._generate_key("embedding", text)
        return await self.set(key, embedding, ttl=86400)
