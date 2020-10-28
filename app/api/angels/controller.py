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
    return await AngelDto.from_orm(angel)
