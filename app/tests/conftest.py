"""
Pytest Fixtures
"""

# Built in
from uuid import uuid4

# Test tools
import pytest

# Utils
from api.utils.security import create_access_token
from fastapi.testclient import TestClient

from app.config import settings

# App server
from app.main import app


@pytest.fixture(scope="module")
def client():
    """Test client."""
    client = TestClient(app)
    yield client


@pytest.fixture()
def app_settings():
    """App settings."""
    return settings


@pytest.fixture()
def get_token():
    """
    Return a function to generate a token
    """

    def access_toke(email):
        token = create_access_token(email, short_duration=True)
        return token

    return access_toke


@pytest.fixture()
def user_mock():
    """Return the test user."""
    return {
        "email": f"test{uuid4()}@gmail.com",
        "password": "user123",
        "firstname": "Stan",
        "lastname": "Lee",
    }


@pytest.fixture()
def profile_mock():
    """Return the test user profile."""
    return {
        "phone": "5512369856",
        "cel": "+525516963478",
        "photo": "",
        "address": {
            "city": "CDMX",
            "municipality": "Benito Juarez",
            "neighborhood": "Venados",
            "street": "Popocatepetl",
            "num_int": "5",
            "num_ext": "25",
            "cp": "01596",
        },
    }
