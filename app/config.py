"""
Unu API - Application settings.
"""

from typing import List

from pydantic import BaseSettings

POSTGRES_DB_URL = "postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"


class PostgresSettings(BaseSettings):
    """Postgres env values."""

    class Config:
        """Get env variables from dotenv file."""

        env_file = ".env"

    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    POSTGRES_SERVER: str


class Settings(BaseSettings):
    """General Application settings class."""

    class Config:
        """Get env variables from dotenv file."""

        env_file = ".env"

    ##########################
    # General Configurations #
    ##########################

    APP_NAME: str = "Mosyne - API"
    API_PREFIX: str = "/api"
    CORS_ORIGIN: List[str]
    EMAIL_ADMIN: str
    WEB_HOST: str
    DEBUG_MODE: bool

    ############
    # Security #
    ############

    SECRET_JWT: str
    COOKIE_SESSION_NAME: str = "oreo_session"
    COOKIE_SESSION_AGE: int = 60 * 60 * 24 * 7 * 4  # One month

    ############
    # DataBase #
    ############

    POSTGRES = PostgresSettings()
    DB_URL: str = POSTGRES_DB_URL.format(**POSTGRES.dict())
    DB_MODELS: List[str] = [
        "api.users.models.user",
        "api.users.models.address",
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

    SENDGRID_API_KEY: str
    EMAIL_SENDER: str

    ################
    # File Storage #
    ################

    GOOGLE_STORAGE_BUCKET: str
    ALLOWED_EXTENSIONS: List[str]
    GOOGLE_APPLICATION_CREDENTIALS: str


settings = Settings()
