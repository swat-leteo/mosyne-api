"""
Controller - Auth bussiness logic.
"""

# Models
from api.users.models import Address, User
from api.users.schema import UserDto

# Exceptions
from api.utils import exceptions

# Security utils
from api.utils.security import get_from_token, hash_password, verify_password
from tortoise.exceptions import IntegrityError

# Schemas
from .schema import SignupInfo


async def signup(user_info: SignupInfo) -> User:
    """Register a new user.

    Params:
    -------
    - user_info: SingupInfo - The user info

    Return:
    -------
    - user: User - a User instance.
    """
    user_data = user_info.dict()

    hashed_password = hash_password(user_info.password)
    user_data.update({"password": hashed_password})
    try:
        user = await User.create(**user_data)
        user.address = await Address.create()
        await user.save()
    except IntegrityError:
        return exceptions.conflict_409("Email already exist")
    return user


async def login(email: str, password: str) -> UserDto:
    """Validate user credentials and return user info.

    Params:
    -------
    - email: str - User email address.
    - password: str - User raw password.

    Return:
    -------
    - user: UserDto - User info.
    """
    user = await User.filter(email=email).first()
    if not user:
        return exceptions.unauthorized_401()
    if not verify_password(password, user.password):
        return exceptions.unauthorized_401()
    if not user.is_verified:
        return exceptions.precondition_failed_412("First confirm your email")

    return await UserDto.from_tortoise_orm(user)


async def confirm_email(token: str) -> None:
    """Change the status of "is_verified" to True.

    Params:
    -------
    - token: str - Verification token.
    """
    email = get_from_token(token)
    user = await User.filter(email=email).first()
    if not user:
        return exceptions.not_found_404("User not found.")

    user.is_verified = True
    await user.save()


async def reset_password(token: str, password: str) -> None:
    """Reset password and return the user.

    Params:
    -------
    - token: str - Email token.
    - password: str - User new raw password.

    Return:
    -------
    - user: UserDto - User info.
    """
    email = get_from_token(token)
    user = await User.filter(email=email).first()
    if not user:
        return exceptions.not_found_404("User not found.")

    user.password = hash_password(password)
    await user.save()
