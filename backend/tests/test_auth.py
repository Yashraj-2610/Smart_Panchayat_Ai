"""
Test authentication endpoints
"""
def test_user_registration_and_login(client):
    """Test user registration and login flow"""
    # Register new user
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "securepass123",
        "full_name": "New User",
        "role": "Family Head"
    }

    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201
    assert "access_token" in response.json()
    assert response.json()["user"]["username"] == "newuser"

    # Login with same credentials
    login_data = {
        "username_or_email": "newuser",
        "password": "securepass123"
    }

    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["user"]["username"] == "newuser"


def test_duplicate_registration(client):
    """Test that duplicate username/email fails"""
    user_data = {
        "username": "duplicate",
        "email": "duplicate@example.com",
        "password": "pass123",
        "full_name": "Duplicate User",
        "role": "Family Head"
    }

    # First registration
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201

    # Duplicate username
    user_data["email"] = "different@example.com"
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 400
    assert "already taken" in response.json()["detail"]

    # Duplicate email
    user_data["username"] = "differentuser"
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_invalid_login(client):
    """Test login with invalid credentials"""
    # Non-existent user
    response = client.post(
        "/api/v1/auth/login",
        json={"username_or_email": "nonexistent", "password": "wrongpass"}
    )
    assert response.status_code == 401

    # Wrong password
    response = client.post(
        "/api/v1/auth/login",
        json={"username_or_email": "sarpanch", "password": "wrongpass"}
    )
    assert response.status_code == 401