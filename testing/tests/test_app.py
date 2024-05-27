## testing the app.py file. Testing endpoint /register and /login using pytest.
import pytest
from app import app

def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_register_user(client):
    response = client.post("/register", data={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "You have successfully registered" in response.data


def test_login_user(client):
    response = client.post("/login", data={
        "username": "testuser",
        "password": "password123"
    })
    assert response.status_code == 302
    assert "Logged in successfully" in response.data
