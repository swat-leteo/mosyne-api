"""
Schemas - User Schemas
"""

# Typing
from typing import Optional

# Setting
from config import settings

# Pydantic
from pydantic import BaseModel, Field

# Tortoise ORM
from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

# User model
from .models import Address, User

# Init models to get all related fields
Tortoise.init_models(settings.DB_PATHS, app_label="models")

###################
# Address Schemas #
###################

AddressDto = pydantic_model_creator(
    Address,
    exclude=("users", "id", "angel_profile", "created", "updated"),
)


################
# User Schemas #
################

UserDto = pydantic_model_creator(User, exclude=("angels", "password", "is_verified"))


class UserUpdateDto(BaseModel):
    """Body schema for update user info."""

    email: str = Field(..., example="stan@marvel.com")
    firstname: str = Field(..., example="Stan")
    lastname: str = Field("", example="Lee")

    phone: str = Field("", example="5512369856")
    cel: str = Field("", example="+525516963478")

    photo: str = Field(..., example="https://mosine.googlestorage.2515-1515-145")

    address: Optional[AddressDto]
