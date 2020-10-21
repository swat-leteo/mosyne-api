"""
Schemas - User Schemas
"""

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
Tortoise.init_models(settings.DB_MODELS, app_label="models")

###################
# Address Schemas #
###################

AddressDto = pydantic_model_creator(Address)


class AddressInDto(BaseModel):
    """Schema to register/update user address."""

    city : str = Field(...)
    muicipality : str = Field(...)
    neighborhood : str = Field(...)
    street : str = Field(...)
    num_int : str = Field(...)
    num_ext : str = Field(...)
    cp : str = Field(...)



################
# User Schemas #
################

UserDto = pydantic_model_creator(User)


class UserUpdateDto(BaseModel):
    """Body schema for update user info."""

    email: str = Field(example="stan@marvel.com")
    firstname: str = Field(example="Stan")
    lastname: str = Field(example="Lee")
    phone: str = Field(example="5512369856")
    cel: str = Field(example="+525516963478")
    photo: str = Field(example="base64_encode-image")

    address: AddressInDto
