"""
Schemas - Auth Schemas
"""



from pydantic import BaseModel, Field

from users.models import User

from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

UserDto = pydantic_model_creator(User)

class Credentials(BaseModel):
    email: str = Field(...)
    password: str = Field(...)