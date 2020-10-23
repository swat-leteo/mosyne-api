"""
Schemas - Auth Schemas
"""

# User schema
from api.users import schema

# Pydantic
from pydantic import BaseModel, Field

################
# Auth Schemas #
################


class LoginCredentials(BaseModel):
    """Body schema for login a user."""

    email: str = Field(..., example="stan@marvel.com")
    password: str = Field(..., example="Marvel123")


class SignupInfo(LoginCredentials):
    """Body schema for create user."""

    firstname: str = Field(..., example="Stan")
    lastname: str = Field(..., example="Lee")


class UserDto(schema.UserDto):
    """Only inherit from UserDto."""
