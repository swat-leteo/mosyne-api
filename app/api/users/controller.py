"""
Controller - Users bussiness logic.
"""

# Built in
from uuid import UUID

# Exceptions
from api.utils import exceptions

# Storage
from services.storage import get_or_update_image

# Db exceptions
from tortoise.exceptions import DoesNotExist, IntegrityError

# Models
from .models import Address, User

# Schema & Models
from .schema import UserDto, UserUpdateDto


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

        address = user_data.address
        user_data_dict = user_data.dict()
        user_data_dict.pop("address")

        user.update_from_dict(user_data_dict)
        await user.save()

        if address:
            user_address = await Address.filter(users=user.id).first()
            user_address.update_from_dict(address.dict())
            await user_address.save()

    except IntegrityError:
        return exceptions.conflict_409("Email already exists")

    return await UserDto.from_tortoise_orm(user)


async def delete_user(user_id: UUID) -> None:
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


async def get_guardian_email(guardian_id: UUID, angel_name: str) -> str:
    """Return the email of the angel guardian.

    Params:
    -------
    - guardian_id: UUID - The angel id.
    - angel_name: str - The angel name.

    Return:
    -------
    - email: str - The guardian email.
    """
    try:
        user = await User.get(id=guardian_id)
    except DoesNotExist:
        return False

    angels = await user.fetch_related("angels")
    for angel in angels:
        if angel.name == angel_name:
            return user.email
    return False
