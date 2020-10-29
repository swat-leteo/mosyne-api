"""
Controller - Angels bussiness logic.
"""

from typing import List

# Security utils
from api.utils import exceptions

# Exceptions
from tortoise.exceptions import IntegrityError
from users.models import Address, User

# models
from .models import Angel  # Al crear un ángel se crea un contacto
from .models import Contact

# Usa nombres concistentes como los que ya hemos creado
from .schema import AngelCreateDto, AngelDto, ContactDto


async def create_angel(
    angel_info: AngelCreateDto, user: User, contacts: List[ContactDto]
) -> AngelDto:
    angel_data = angel_info.dict()
    address_data = angel_data.get("address")
    angel_data.pop("address")
    try:
        angel = await Angel.create(**angel_data)
        address = await Address.create(**address_data)
        angel.guardian = user
        angel.address = address

        for contact in contacts:
            contact = await Contact.create(**contact.dict(), angel=angel)

        await angel.save()

    except IntegrityError:
        return exceptions.conflict_409("Something Wrong")
    return await AngelDto.from_tortoise_orm(angel)


async def get_angel_id(angel_id: int) -> AngelDto:
    try:
        angel = await Angel.get(id=id)
    except IntegrityError:
        return exceptions.not_found_404("The angel does not exist")
    return AngelDto.from_tortoise_orm(angel)


async def update_angel_data(angel_id: int, angel_data: AngelDto) -> AngelDto:
    try:
        angel = await Angel.get(id=angel_id)
        angel_data_dict = angel_data.dict()
        angel.update_from_dict(angel_data_dict)
        await angel.save()
    except IntegrityError:
        return exceptions.conflict_409("Something was wrong")
    return AngelDto.from_tortoise_orm(angel)


async def delete_angel_data(angel_id: int) -> None:
    try:
        angel = Angel.get(id=angel_id)
        await angel.delete()
    except IntegrityError:
        return exceptions.not_found_404("Angel does not exist")
