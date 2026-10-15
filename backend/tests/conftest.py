"""
Pytest configuration and fixtures for Smart Panchayat AI tests
"""
import os
import sys
import pytest
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from fastapi.testclient import TestClient

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.core.database import Base, get_db
from app.core.config import settings
from app.main import app
from app.models.user import User, UserRole
from app.core.security import hash_password


# Use in-memory SQLite for tests
TEST_DATABASE_URL = "sqlite:///./test_smart_panchayat.db"
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=None  # NullPool for tests
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


@pytest.fixture(scope="session")
def db_engine():
    """Create database tables for test session"""
    Base.metadata.create_all(bind=test_engine)
    yield test_engine
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def db_session(db_engine) -> Generator[Session, None, None]:
    """Create a new database session for each test"""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Create a test client with database override"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session: Session) -> User:
    """Create a test user"""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=hash_password("testpass123"),
        full_name="Test User",
        role=UserRole.FAMILY_HEAD,
        phone_number="+919876543210",
        preferred_language="en",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_sarpanch(db_session: Session) -> User:
    """Create a test sarpanch user"""
    user = User(
        username="testsarpanch",
        email="sarpanch@test.gov.in",
        hashed_password=hash_password("sarpanch123"),
        full_name="Test Sarpanch",
        role=UserRole.SARPANCH,
        phone_number="+919876543211",
        preferred_language="mr",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(client: TestClient, test_user: User) -> dict:
    """Get authentication headers for test user"""
    response = client.post(
        "/api/v1/auth/login",
        json={"username_or_email": test_user.username, "password": "testpass123"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sarpanch_headers(client: TestClient, test_sarpanch: User) -> dict:
    """Get authentication headers for sarpanch user"""
    response = client.post(
        "/api/v1/auth/login",
        json={"username_or_email": test_sarpanch.username, "password": "sarpanch123"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}