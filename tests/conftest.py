"""Pytest fixtures for testing with in-memory SQLite."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.database import Base
from api.main import app

# Import models to ensure they are registered with Base.metadata
from api.models import Greeting  # noqa: F401


@pytest.fixture(scope="function")
def test_db():
    """Create an in-memory SQLite database for testing.
    
    Using file:test.db?mode=memory&cache=shared to ensure all connections
    share the same in-memory database.
    """
    # Use shared cache mode for in-memory SQLite
    engine = create_engine(
        "sqlite:///file:test.db?mode=memory&cache=shared",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    def get_test_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    # Override the app's database dependency
    from api.database import get_db_session
    app.dependency_overrides[get_db_session] = get_test_db
    
    yield {"engine": engine, "SessionLocal": SessionLocal}
    
    # Cleanup
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def client(test_db):
    """Create a test client with the test database."""
    from fastapi.testclient import TestClient
    return TestClient(app)
