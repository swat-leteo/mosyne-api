"""
Router - Users routes.
"""

from typing import Optional

# Typing
from uuid import UUID

# Responses
from api.utils import responses
from api.utils.security import get_auth_user

# FastAPI
from fastapi import APIRouter, BackgroundTasks, Depends

# Email
from services.mails import send_angel_advise

# Controller
from .controller import complete_profile, current_user, delete_user, update_user

# Schemas
from .schema import UserDto, UserProfile, UserUpdateDto

###############
# User router #
###############

router = APIRouter()


@router.post(
    "",
    status_code=201,
    responses={
        "201": {"model": UserDto},
        "401": {"model": responses.Unauthorized},
        "403": {"model": responses.Forbidden},
    },
)
async def retrieve_user(
    user_profile: UserProfile, user=Depends(get_auth_user)
) -> UserDto:
    """Retrieve a user by id."""
    user_retrieved = await complete_profile(user.id, user_data)
    return user_retrieved


@router.get(
    "",
    status_code=200,
    responses={
        "200": {"model": UserDto},
        "401": {"model": responses.Unauthorized},
        "403": {"model": responses.Forbidden},
    },
)
async def get_current_user(user=Depends(get_auth_user)) -> UserDto:
    """Retrieve data of the current logged user."""
    return await current_user(user)


@router.put(
    "",
    status_code=200,
    responses={
        "200": {"model": UserDto},
        "401": {"model": responses.Unauthorized},
        "403": {"model": responses.Forbidden},
        "404": {"model": responses.Forbidden},
        "409": {"model": responses.Conflict},
    },
)
async def update_user_info(
    user_info: UserUpdateDto, user=Depends(get_auth_user)
) -> UserDto:
    """Update the info of existing user."""
    user_updated = await update_user(user.id, user_info)
    return user_updated


@router.delete(
    "",
    status_code=200,
    responses={
        "200": {"model": responses.Msg},
        "401": {"model": responses.Unauthorized},
        "403": {"model": responses.Forbidden},
        "404": {"model": responses.NotFound},
    },
)
async def delete_existing_user(user=Depends(get_auth_user)) -> responses.Msg:
    """Delete a existing user that matches th passed id."""
    result = await delete_user(user.id)
    return result


@router.post(
    "/angel-advise/{guardian_id}",
    status_code=200,
    responses={
        "200": {"model": responses.EmailMsg},
        "401": {"model": responses.Unauthorized},
        "403": {"model": responses.Forbidden},
    },
)
async def send_email_for_angel(
    guardian_id: UUID,
    angel_name: str,
    lat: Optional[str],
    lon: Optional[str],
    background_task: BackgroundTasks,
) -> responses.EmailMsg:
    """Send a email to the guardian when his/her angel profile is visited."""
    email = await get_guardian_email(guardian_id)

    if email:
        background_task.add_task(
            send_angel_advise, email=email, angel_name=angel_name, lat=lat, lon=lon
        )
    return responses.EmailMsg("Email sent")
