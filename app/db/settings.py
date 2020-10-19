"""
DB config file.
"""

from config import settings

TORTOISE_ORM_CONFIG: dict = {
    "connections": {
        "default": settings.DB_URL,
    },
    "apps": {
        "models": {"models": settings.DB_MODELS},
    },
}
