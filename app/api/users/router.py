"""
Router - Users routes.
"""

from typing import Optional

# Typing
from uuid import UUID

# Responses
from api.utils import responses
from api.utils.responses import create_responses
from api.utils.security import get_auth_user

# FastAPI
from fastapi import APIRouter, BackgroundTasks, Depends

# Email
from services.mails import send_angel_advise

# Controller
from .controller import current_user, delete_user, get_guardian_email, update_user

# Schemas
from .schema import UserDto, UserUpdateDto

###############
# User router #
###############

router = APIRouter()


@router.get(
    "",
    status_code=200,
    response_model=UserDto,
    responses=create_responses([401, 403]),
)
async def get_current_user(user=Depends(get_auth_user)) -> UserDto:
    """Retrieve data of the current logged user."""
    return await current_user(user)


@router.put(
    "",
    status_code=200,
    response_model=UserDto,
    responses=create_responses([401, 403, 409]),
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
    response_model=responses.Msg,
    responses=create_responses([401, 403, 404]),
)
async def delete_existing_user(user=Depends(get_auth_user)) -> responses.Msg:
    """Delete a existing user that matches th passed id."""
    await delete_user(user.id)
    return responses.Msg(detail="User deleted")


@router.post(
    "/angel-advise/{guardian_id}",
    status_code=200,
    response_model=responses.EmailMsg,
    responses=create_responses([401, 403]),
)
async def send_email_for_angel(
    guardian_id: UUID,
    angel_name: str,
    background_task: BackgroundTasks,
    lat: Optional[str] = None,
    lon: Optional[str] = None,
) -> responses.EmailMsg:
    """Send a email to the guardian when his/her angel profile is visited."""
    email = await get_guardian_email(guardian_id, angel_name)

    if email:
        background_task.add_task(
            send_angel_advise, email=email, angel_name=angel_name, lat=lat, lon=lon
        )
    return responses.EmailMsg(detail="Email sent")
