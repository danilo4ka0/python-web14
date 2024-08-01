import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_route():
    response = client.post("/register", json={"email": "test@example.com", "password": "testpassword"})
    assert response.status_code == 200
    assert response.json() == {"msg": "Please verify your email"}

def test_register_existing_route():
    client.post("/register", json={"email": "existing@example.com", "password": "testpassword"})
    response = client.post("/register", json={"email": "existing@example.com", "password": "testpassword"})
    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists"}
