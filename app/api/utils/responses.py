"""
General API responses.

This classes are used for route documentation.
"""

# Typing
from typing import Dict, List

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


#########################
# Responses constructor #
#########################


def create_responses(list_status_responses: List[str]) -> Dict[str, dict]:
    """Create a dictionary with the response models according to its http status.

    Params:
    -------
    - list_status_response: Lits[str] - A list with desired status code responses.

    Return:
    -------
    - responses: dict - A dictionary with desired responses.
    """
    map_status_to_model = {
        400: BadRequest,
        401: Unauthorized,
        403: Forbidden,
        404: NotFound,
        409: Conflict,
        412: PreconditionFailed,
    }

    responses = {}

    try:
        for status in list_status_responses:
            responses[status] = {"model": map_status_to_model[status]}
    except KeyError:
        raise Exception("Only status: [400, 401, 403, 404, 409, 412] are allowed.")

    return responses
