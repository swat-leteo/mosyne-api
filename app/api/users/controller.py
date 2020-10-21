"""
Controller - Users bussiness logic.
"""

# Built in
from uuid import UUID

# Exceptions
from api.utils import exceptions
from tortoise.exceptions import DoesNotExist, IntegrityError

# Models
from .models import Address, User

# Schema & Models
from .schema import AddressDto, AddressInDto, UserDto, UserUpdateDto


async def update_user(user_data: UserUpdateDto, user_id: UUID) -> UserDto:
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
        user = await user.update_from_dict(user_data.dict())
    except DoesNotExist:
        return exceptions.not_found_404('User not found')
    except IntegrityError:
        return exceptions.conflict_409('Email already exists')

    return await UserDto.from_tortoise_orm(user)
