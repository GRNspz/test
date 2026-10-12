import pytest
from fastapi.testclient import TestClient
from api.main import app

@pytest.fixture
def client():
    return TestClient(app)


def test_root_route(client):
    """Test that the root route returns HTML with the form"""
    response = client.get("/")
    assert response.status_code == 200
    assert "<input type=\"text\" id=\"name\"" in response.text
    assert "<button type=\"submit\">" in response.text
    assert "Hallo Web App" in response.text


def test_hello_endpoint_with_name(client):
    """Test that the /api/hello endpoint returns the correct greeting"""
    response = client.post(
        "/api/hello",
        data={"name": "Max"}
    )
    assert response.status_code == 200
    assert response.text == "Hallo, Max!"


def test_hello_endpoint_with_empty_name(client):
    """Test that the /api/hello endpoint returns greeting with empty name"""
    response = client.post(
        "/api/hello",
        data={"name": ""}
    )
    assert response.status_code == 200
    assert response.text == "Hallo, !"


def test_hello_endpoint_with_special_characters(client):
    """Test that the /api/hello endpoint handles special characters"""
    response = client.post(
        "/api/hello",
        data={"name": "Müller & co"}
    )
    assert response.status_code == 200
    assert response.text == "Hallo, Müller & co!"


def test_hello_endpoint_missing_name(client):
    """Test that the /api/hello endpoint handles missing name with default empty string"""
    response = client.post("/api/hello")
    assert response.status_code == 200
    assert response.text == "Hallo, !"
