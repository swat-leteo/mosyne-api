"""
Schemas - Auth Schemas
"""


from pydantic import BaseModel, Field

################
# Auth Schemas #
################


class LoginCredentials(BaseModel):
    email: str = Field(...)
    password: str = Field(...)


class SignupInfo(BaseModel):
    email: str = Field(...)
    passsword: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
