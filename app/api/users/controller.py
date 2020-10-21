"""
Controller - Users bussiness logic.
"""

# Built in
from uuid import UUID

# Exceptions
from api.utils import exceptions, responses

# Storage
from services.storage import get_or_update_image

# Db exceptions
from tortoise.exceptions import DoesNotExist, IntegrityError, OperationalError

# Models
from .models import Address, User

# Schema & Models
from .schema import UserDto, UserProfile, UserUpdateDto


async def complete_profile(user_id: UUID, user_data: UserProfile) -> UserDto:
    """Retrieve a user.

    Params:
    -------
    - user_id: UUID - The user pk.
    - user_data: UserProfile - The data to complete the profile

    Return:
    -------
    - user: UserDto - The user info.
    """
    if user_data.photo:
        user_data.photo = get_or_update_image(user_data.photo)
    try:
        user = await User.get(id=user_id)

        user.address = await Address.create(**user_data.address.dict())
        user.update_from_dict(user_data.dict())
        await user.save()
    except (IntegrityError, OperationalError):
        return exceptions.server_error_500()

    return await UserDto.from_tortoise_orm(user)


async def current_user(user: User) -> UserDto:
    """Return a instance of the UserDto of current user model.

    Params:
    -------
    - user: User - The user model instance.

    Return:
    -------
    - user: UserDto - The user info.
    """
    return await UserDto.from_tortoise_orm(user)


async def update_user(user_id: UUID, user_data: UserUpdateDto) -> UserDto:
    """Update a user.

    Params:
    -------
    - user_data: UserUpdateDto - The new data to update.
    - user_id: UUID - The user pk.

    Return:
    -------
    - user: UserDto - The user updated.
    """
    if user_data.photo:
        user_data.photo = get_or_update_image(user_data.photo)
    try:
        user = await User.get(id=user_id)

        user_data.photo = get_or_update_image(user_data.photo)
        user.update_from_dict(user_data.dict())
        await user.save()
    except IntegrityError:
        return exceptions.conflict_409("Email already exists")

    return await UserDto.from_tortoise_orm(user)


async def delete_user(user_id: UUID) -> responses.Msg:
    """Update a user.

    Params:
    -------
    - user_data: UserUpdateDto - The new data to update.
    - user_id: UUID - The user pk.

    Return:
    -------
    - user: UserDto - The user updated.
    """

    try:
        user = await User.get(id=user_id)
        await user.delete()
    except DoesNotExist:
        return exceptions.not_found_404("User not found")

    return responses.Msg("User deleted")


async def get_guardian_email(guardian_id: UUID) -> str:
    """Return the email of the angel guardian.

    Params:
    -------
    - guardian_id: UUID - The angel id.

    Return:
    -------
    - email: str - The guardian email.
    """
    user = await User.get(id=guardian_id)
    return user.email
