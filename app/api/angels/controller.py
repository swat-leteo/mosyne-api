"""
Controller - Angels bussiness logic.
"""

# Typing
from typing import List
from uuid import UUID

# Util Models/Schemas
from api.users.schema import Address, User, UserDto

# Security utils
from api.utils import exceptions

# Config
from config import settings

# Qr
from services.qr import generate_qr_base64_web

# Exceptions
from tortoise.exceptions import DoesNotExist, IntegrityError

# Angel - Models and Schema
from .models import Angel, Contact
from .schema import (
    AngelCreateDto,
    AngelDto,
    AngelListDto,
    AngelQrDto,
    AngelUpdateDto,
    ContactDto,
)


async def create_angel(
    angel_info: AngelCreateDto,
    contacts: List[ContactDto],
    im_my_guardian: bool,
    use_guardian_address: bool,
    user: User,
) -> AngelDto:
    """Create a new angel and all his/her emergency contacts.

    Params:
    -------
    - angel_info: AngelCreateDto - The angel data.
    - contacts: List[ContactDto] - An array of emergency contacts.
    - user: User - The current user (tortoise model instance).
    - im_my_guardian: bool - Indicates if the user is its own angel.
    - use_guardian_address: bool - Indicates if the angel address is the same as user.

    Return:
    -------
    - angel: AngelDto - The new angel.
    """
    angel_data = angel_info.dict()
    address_data = angel_data.get("address")
    angel_data.pop("address")

    try:
        if use_guardian_address or im_my_guardian:
            user_dto = await UserDto.from_tortoise_orm(user)
            if not user.address.id:
                return exceptions.precondition_failed_412("Guardian don´t have address")
            address_data = user_dto.address.dict()

        address = await Address.create(**address_data)
        angel = await Angel.create(**angel_data, guardian=user, address=address)

        # Create all related contacts
        for contact in contacts:
            await Contact.create(**contact.dict(), angel=angel)
    except IntegrityError as e:
        return exceptions.conflict_409(e.args[0])
    except ValueError as e:
        return exceptions.bad_request_400(e.args[0])
    return await AngelDto.from_tortoise_orm(angel)


async def get_angels_of_user(user: User) -> List[AngelDto]:
    """Retrive all angels associated with the current user.

    Params:
    -------
    - user: User - The current user (model instance).

    Return:
    - angels: List[AngelDto] - A list of angels.
    """
    angels = Angel.filter(guardian=user)
    return await AngelListDto.from_queryset(angels)


async def get_angel(angel_id: UUID) -> AngelDto:
    """Retrieve and angel by Id.

    Params:
    -------
    - angel_id: UUID - The ID of the target angel.

    Return:
    -------
    - angel: AngelDto - The angel info.
    """
    try:
        angel = await Angel.get(id=angel_id).prefetch_related("address")
    except DoesNotExist:
        return exceptions.not_found_404("The angel does not exist")
    return await AngelDto.from_tortoise_orm(angel)


async def update_angel(angel_id: UUID, angel_info: AngelUpdateDto) -> AngelDto:
    """Update angel info.

    Params:
    -------
    - angel_id: UUID - The angel ID.
    - angel_data: AngelUpdateDto - The info to update.

    Return:
    -------
    - angel: AngelDto - The updated angel.
    """
    angel_data: dict = angel_info.dict()
    address_data = angel_data.get("address")
    angel_data.pop("address")

    try:
        angel = await Angel.get(id=angel_id)
        angel.update_from_dict(angel_data)
        await angel.save()

        if address_data:
            address = await Address.get(id=angel.address_id)
            address.update_from_dict(address_data)
            await address.save()
    except DoesNotExist:
        return exceptions.not_found_404("Angel not found")
    except IntegrityError as e:
        return exceptions.conflict_409(e.args[0])

    angel_updated = await Angel.get(id=angel_id).prefetch_related("address")
    return await AngelDto.from_tortoise_orm(angel_updated)


async def update_angel_contact(contact_id: UUID, contact_info: ContactDto) -> AngelDto:
    """Update an angel contact data and return the angel updated.

    Params:
    -------
    - contact_id: UUID - The contact ID.
    - contact_info: ContactDto - The contact data to update.

    Return:
    -------
    - angel: AngelDto - The angel updated.
    """
    try:
        contact = await Contact.get(id=contact_id)
        contact.update_from_dict(contact_info.dict())
        await contact.save()
    except DoesNotExist:
        return exceptions.not_found_404("Contact not found")
    except IntegrityError as e:
        return exceptions.conflict_409(e.args[0])

    angel = await Angel.get(id=angel_id).prefetch_related("address")
    return await AngelDto.from_tortoise_orm(angel)


async def delete_angel(angel_id: UUID) -> None:
    """Delete an angel by ID.

    Params:
    -------
    - angel_id: UUID - The angel ID.
    """
    try:
        angel = await Angel.get(id=angel_id)
        await angel.delete()
    except DoesNotExist:
        return exceptions.not_found_404("Angel does not exist")


async def get_qr_code(angel_id: UUID) -> AngelQrDto:
    """Generate a QR code image to the angel profile.

    Params:
    -------
    - angel_ud: UUID - The angel id.

    Return:
    -------
    - qr_image: AngelQrDto - The qr code image in base64 format.
    """
    try:
        angel = await Angel.get(id=angel_id)
    except DoesNotExist:
        return exceptions.not_found_404("Angel not found")

    angel_url = f"{settings.WEB_HOST}/angels/{angel.id}"
    qr_image = generate_qr_base64_web(url=angel_url)
    return AngelQrDto(qr_image=qr_image)
