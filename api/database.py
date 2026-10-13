"""Database session management and engine configuration."""

import os
from contextlib import contextmanager
from typing import Generator, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# SQLAlchemy base class for models
class Base(DeclarativeBase):
    pass


# Global engine - created once and reused
_engine: Optional[object] = None


def get_database_url():
    """Get the database URL from environment or settings."""
    # Try to get from environment variable first (for alembic and tests)
    db_url = os.environ.get("DATABASE_URL")
    if db_url:
        return db_url
    
    # Fall back to settings
    from api.config import settings
    return settings.database_url


def _create_engine(db_url):
    """Create an engine from a database URL."""
    # For SQLite in-memory, we need to handle it differently
    if db_url.startswith("sqlite"):
        return create_engine(
            db_url,
            connect_args={"check_same_thread": False},
        )
    else:
        # For PostgreSQL with pooler (Vercel), disable prepared statements
        return create_engine(
            db_url,
            pool_pre_ping=True,
            pool_recycle=3600,
            connect_args={"application_name": "hello-web-app"},
        )


def get_engine():
    """Get or create the SQLAlchemy engine."""
    global _engine
    if _engine is None:
        _engine = _create_engine(get_database_url())
    return _engine


def set_engine(engine):
    """Set a custom engine (for testing)."""
    global _engine
    _engine = engine


def reset_engine():
    """Reset the engine (for testing cleanup)."""
    global _engine
    if _engine is not None:
        _engine.dispose()
    _engine = None


def get_session_factory():
    """Get or create the session factory."""
    engine = get_engine()
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db() -> Generator[Session, None, None]:
    """Provide a database session."""
    SessionLocal = get_session_factory()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_session():
    """FastAPI dependency for database session."""
    SessionLocal = get_session_factory()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# For alembic to access Base without triggering engine creation
# This is safe because Base doesn't require the engine
def get_base():
    """Get the Base class for alembic."""
    return Base
