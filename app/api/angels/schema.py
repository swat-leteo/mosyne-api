"""
Schemas - Angel Schemas
"""

# Typing
from typing import List, Optional
from uuid import UUID

# Aditional Schemas
from api.users.schema import AddressDto

# Settings
from config import settings

# Pydantic
from pydantic import BaseModel, Field

# Tortoise ORM
from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

# Models
from .models import Angel, Contact

# Init models to get all related fields
Tortoise.init_models(settings.DB_PATHS, app_label="models")


###################
# Contact Schemas #
###################

ContactDto = pydantic_model_creator(
    Contact,
    exclude=(
        "id",
        "angel",
        "angel_id",
        "created",
        "updated",
    ),
)


class ContactDtoAngel(ContactDto):
    """Contact schema in angel body."""

    id: UUID = Field(...)


##################
# Angels Schemas #
##################

AngelDtoBase = pydantic_model_creator(Angel, exclude=("guardian",))

AngelCreateDtoBase = pydantic_model_creator(
    Angel,
    exclude=(
        "id",
        "guardian",
        "contacts",
        "address",
        "guardian_id",
        "address_id",
        "created",
        "updated",
    ),
)

AngelListDto = pydantic_queryset_creator(Angel, exclude=("guardian",))


class AngelDto(AngelDtoBase):
    """Angel Schema."""

    photo: str = Field(..., example="https://mosine.googlestorage.2515-1515-145")
    address: AddressDto
    surgeries: List[str] = Field(...)
    alergies: List[str] = Field(...)
    medicines: List[str] = Field(...)
    contacts: List[ContactDtoAngel]


class AngelCreateDto(AngelCreateDtoBase):
    """Body schema for create an angel."""

    photo: str = Field(..., example="https://mosine.googlestorage.2515-1515-145")
    surgeries: List[str] = Field([])
    alergies: List[str] = Field([])
    medicines: List[str] = Field([])
    address: Optional[AddressDto]


class AngelUpdateDto(AngelCreateDto):
    """Body Schema for update and angel."""


class AngelQrDto(BaseModel):
    """Body Schema of QR response."""

    qr_image: str = Field(
        ...,
        example="data:image/png;base64,mFAZ21haWwuY29tPgotIEphaXIgw4FndWl",
    )
