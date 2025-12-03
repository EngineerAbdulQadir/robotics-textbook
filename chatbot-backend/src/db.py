"""Database configuration and session management."""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from .config import settings

# Global engine and session factory (lazy-loaded)
_engine: Optional[object] = None
_AsyncSessionLocal: Optional[object] = None


def _get_engine():
    """Get or create database engine with optimized settings."""
    global _engine
    if _engine is None:
        from sqlalchemy.ext.asyncio import create_async_engine
        _engine = create_async_engine(
            settings.neon_database_url,
            echo=settings.debug,
            future=True,
            pool_size=settings.database_pool_size,
            max_overflow=settings.database_max_overflow,
            pool_recycle=3600,  # Recycle connections after 1 hour to handle DB idle timeouts
            pool_pre_ping=True,  # Test connections before using them
        )
    return _engine


def _get_session_factory():
    """Get or create async session factory."""
    global _AsyncSessionLocal
    if _AsyncSessionLocal is None:
        from sqlalchemy.ext.asyncio import async_sessionmaker
        _AsyncSessionLocal = async_sessionmaker(
            _get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return _AsyncSessionLocal


async def get_db() -> AsyncSession:
    """Get database session dependency."""
    async with _get_session_factory()() as session:
        yield session


# Export for external use
def get_engine():
    """Get database engine."""
    return _get_engine()
