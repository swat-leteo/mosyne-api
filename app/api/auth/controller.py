"""
Controller - Auth bussiness logic.
"""

# Exceptions
from api.utils import exceptions
from tortoise.exceptions import DoesNotExist, IntegrityError

from users.models import User
from .schema import Credentials

async def login_user(email, password):
    user = await User.filter(email=email).first()
    if not user:
        return exceptions.unauthorized_401()
    return user