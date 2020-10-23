"""
Pytest Fixtures
"""

# Built in
import os
from uuid import uuid4

# Test tools
import pytest

# Utils
from api.utils.security import create_access_token
from config import settings
from fastapi.testclient import TestClient

# App server
from main import app
from tortoise.contrib.test import finalizer, initializer


@pytest.fixture(scope="module")
def client():
    """Test client."""
    db_url = f"postgres://postgres:postgres@localhost:5432/testing"
    if os.getenv("TESTING", False):
        initializer(settings.DB_MODELS, db_url=db_url)
    else:
        initializer(settings.DB_MODELS)
    with TestClient(app) as c:
        yield c
    finalizer()


@pytest.fixture()
def app_settings():
    """App settings."""
    return settings


@pytest.fixture()
def get_token():
    """
    Return a function to generate a token
    """

    def _access_token(email):
        token = create_access_token(email)
        return token

    return _access_token


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
        "password": "user123",
        "firstname": "Stan",
        "lastname": "Lee",
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
