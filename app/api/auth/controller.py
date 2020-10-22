"""
Controller - Auth bussiness logic.
"""

# Exceptions
from api.utils import exceptions
from tortoise.exceptions import IntegrityError

# Models
from users.models import User
from users.schema import UserDto

# Auth2
from utils.security import hash_password, verify_password

# Schemas
from .schema import LoginCredentials, SignupInfo


async def login(credentials: LoginCredentials) -> UserDto:
    """
    Login controller

        Params:
        -------
        - credentials: LoginCredentials - Contains email & password

        Return:
        -------
        - userDto - when the auth was succesful.
        - exceptions - Unauthorized_401 wrong credentials
    """
    user = await User.filter(email=credentials.email).first()
    if not user:
        return exceptions.unauthorized_401()
    if not verify_password(credentials.password, user.password):
        return exceptions.unauthorized_401
    return await UserDto.from_tortoise_orm(user)


async def signup(user_info: SignupInfo) -> User:
    """Signup.

    Params:
    -------
    - user_info: SingupInfo - The user info

    Return:
    -------
    - user: User - a User instance.
    """
    user_info.password = hash_password(user_info.password)
    try:
        new_user = await User.create(**user_info.dict())

    except IntegrityError:
        return exceptions.conflict_409("Email already exist")
    return new_user
