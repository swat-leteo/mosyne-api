"""
General API responses.

This classes are used for route documentation.
"""

# Pydantic
from pydantic import BaseModel, Field

##################
# Mixin Response #
##################


class EmailMsg(BaseModel):
    """Email message schema."""

    detail: str = Field(example="Email sent")


class Msg(BaseModel):
    """Any detail operation message schema."""

    detail: str = Field(example="Opertion successfully")


###################
# Error Responses #
###################


class BadRequest(BaseModel):
    """Bad Request model exception."""

    detail: str = Field(example="Invalid request data")


class Unauthorized(BaseModel):
    """Unauthorized model exception."""

    detail: str = Field(example="Invalid credentials")


class Forbidden(BaseModel):
    """Forbidden model exception."""

    detail: str = Field(example="Action Forbidden")


class NotFound(BaseModel):
    """Not Found model exception."""

    detail: str = Field(example="Resource not found")


class Conflict(BaseModel):
    """Conflict model exception."""

    detail: str = Field(example="Entitie name already exists")


class PreconditionFailed(BaseModel):
    """Conflict model exception."""

    detail: str = Field(example="Precondition Failed")
