"""
Unu API - Application settings.
"""

# Built in
import os
from typing import List

# Settings
from pydantic import BaseSettings

# Envs
TESTING = os.getenv("TESTING", False)

# Postgres URL format.
POSTGRES_DB_URL = "postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"


class PostgresSettings(BaseSettings):
    """Postgres env values."""

    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")


class Settings(BaseSettings):
    """General Application settings class."""

    ##########################
    # General Configurations #
    ##########################

    APP_NAME: str = "Mosyne - API"
    API_PREFIX: str = "/api"
    CORS_ORIGIN: List[str] = ["*"]
    EMAIL_ADMIN: str = os.getenv("EMAIL_ADMIN")

    WEB_HOST: str = "https://mosine.vercel.app"
    API_HOST: str = os.getenv("API_HOST", "http://localhost:8080")

    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", False)

    ############
    # Security #
    ############

    SECRET_JWT: str = os.getenv("SECRET_JWT")
    COOKIE_SESSION_NAME: str = "oreo_session"
    COOKIE_SESSION_AGE: int = 60 * 60 * 24 * 7 * 4  # One month

    ############
    # DataBase #
    ############

    POSTGRES = PostgresSettings()
    DB_URL: str = POSTGRES_DB_URL.format(**POSTGRES.dict())
    DB_MODELS: List[str] = [
        "api.users.models.address",
        "api.users.models.user",
        "api.angels.models.angel",
        "api.angels.models.contact",
        "aerich.models",
    ]
    DB_PATHS: List[str] = [
        "api.users.models",
        "api.angels.models",
    ]

    ########################
    # Email Configurations #
    ########################

    SENDGRID_API_KEY: str = os.getenv("SENDGRID_API_KEY") if not TESTING else ""
    EMAIL_SENDER: str = os.getenv("EMAIL_SENDER")

    ################
    # File Storage #
    ################

    GOOGLE_STORAGE_BUCKET: str = os.getenv("GOOGLE_STORAGE_BUCKET")
    ALLOWED_EXTENSIONS: List[str] = os.getenv("ALLOWED_EXTENSIONS")


settings = Settings()
