"""
Router - Users routes.
"""

# Responses
from api.utils import responses

# FastAPI
from fastapi import APIRouter

# Controller
from .controller import update_user

# Schemas
from .schema import UserDto, UserUpdateDto

###############
# User router #
###############

router = APIRouter()


@router.put(
    "/{id}",
    status_code=200,
    responses={
        "200": {"model": UserDto},
        "401": {"model": responses.Unauthorized},
        "404": {"model": responses.NotFound},
        "409": {"model": responses.Conflict},
    },
)
async def update_user_info(user_info: UserUpdateDto, id: str) -> UserDto:
    """Update the info of existing user."""
    user_updated = await update_user(user_info, user_id)
    return user_updated
