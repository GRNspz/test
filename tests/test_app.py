"""Tests for the Hello Web App with database persistence."""

from datetime import datetime

import pytest

from api.models import Greeting


# Tests for root route and basic functionality (don't need database)

def test_root_route(client):
    """Test that the root route returns HTML with the form."""
    response = client.get("/")
    assert response.status_code == 200
    assert "<input type=\"text\" id=\"name\"" in response.text
    assert "<button type=\"submit\">" in response.text
    assert "Hallo Web App" in response.text
    assert "greetingsList" in response.text  # History list should be present


def test_html_page_has_history_section(client):
    """Test that the HTML page includes the history section."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Letzte Begrüßungen" in response.text
    assert "greetingsList" in response.text
    assert "loadHistory" in response.text


# Tests that require database - use test_db fixture


def test_hello_endpoint_with_name(client, test_db):
    """Test that the /api/hello endpoint returns the correct greeting."""
    response = client.post(
        "/api/hello",
        data={"name": "Max"}
    )
    assert response.status_code == 200
    assert response.text == "Hallo, Max!"


def test_hello_endpoint_with_empty_name(client, test_db):
    """Test that the /api/hello endpoint returns greeting with empty name."""
    response = client.post(
        "/api/hello",
        data={"name": ""}
    )
    assert response.status_code == 200
    assert response.text == "Hallo, !"


def test_hello_endpoint_with_special_characters(client, test_db):
    """Test that the /api/hello endpoint handles special characters."""
    response = client.post(
        "/api/hello",
        data={"name": "Müller & co"}
    )
    assert response.status_code == 200
    assert response.text == "Hallo, Müller & co!"


def test_hello_endpoint_missing_name(client, test_db):
    """Test that the /api/hello endpoint handles missing name with default empty string."""
    response = client.post("/api/hello")
    assert response.status_code == 200
    assert response.text == "Hallo, !"


def test_hello_endpoint_saves_to_database(client, test_db):
    """Test that submitting a name saves it to the database."""
    # Submit a name
    response = client.post(
        "/api/hello",
        data={"name": "TestUser"}
    )
    assert response.status_code == 200
    
    # Check that the name was saved in the database
    SessionLocal = test_db["SessionLocal"]
    session = SessionLocal()
    try:
        from sqlalchemy import select
        greetings = session.scalars(select(Greeting)).all()
        assert len(greetings) == 1
        assert greetings[0].name == "TestUser"
        assert greetings[0].created_at is not None
    finally:
        session.close()


def test_hello_endpoint_saves_multiple_names(client, test_db):
    """Test that multiple names are saved correctly."""
    # Submit multiple names
    names = ["Alice", "Bob", "Charlie"]
    for name in names:
        response = client.post(
            "/api/hello",
            data={"name": name}
        )
        assert response.status_code == 200
    
    # Check that all names were saved
    SessionLocal = test_db["SessionLocal"]
    session = SessionLocal()
    try:
        from sqlalchemy import select
        greetings = session.scalars(select(Greeting).order_by(Greeting.id)).all()
        assert len(greetings) == 3
        assert [g.name for g in greetings] == names
    finally:
        session.close()


def test_history_endpoint_returns_last_10(client, test_db):
    """Test that the /api/history endpoint returns the last 10 greetings."""
    # Submit 15 names
    for i in range(15):
        client.post("/api/hello", data={"name": f"User{i}"})
    
    # Get history
    response = client.get("/api/history")
    assert response.status_code == 200
    
    history = response.json()
    # Should return only the last 10
    assert len(history) == 10
    
    # Check that they are in reverse chronological order
    names = [item["name"] for item in history]
    assert names == [f"User{i}" for i in range(14, 4, -1)]


def test_history_endpoint_with_fewer_than_10(client, test_db):
    """Test that the /api/history endpoint returns all greetings when fewer than 10."""
    # Submit 3 names
    for i in range(3):
        client.post("/api/hello", data={"name": f"User{i}"})
    
    # Get history
    response = client.get("/api/history")
    assert response.status_code == 200
    
    history = response.json()
    assert len(history) == 3
    
    # Check order (most recent first)
    names = [item["name"] for item in history]
    assert names == ["User2", "User1", "User0"]


def test_history_endpoint_empty(client, test_db):
    """Test that the /api/history endpoint returns empty list when no greetings."""
    response = client.get("/api/history")
    assert response.status_code == 200
    assert response.json() == []


def test_history_endpoint_response_structure(client, test_db):
    """Test that the /api/history endpoint returns correct structure."""
    # Submit a name
    client.post("/api/hello", data={"name": "TestUser"})
    
    # Get history
    response = client.get("/api/history")
    assert response.status_code == 200
    
    history = response.json()
    assert len(history) == 1
    
    # Check structure of history item
    item = history[0]
    assert "name" in item
    assert "created_at" in item
    assert item["name"] == "TestUser"
    
    # Check that created_at is a valid ISO format datetime
    created_at = item["created_at"]
    # Try to parse the datetime
    datetime.fromisoformat(created_at.replace("Z", "+00:00"))
