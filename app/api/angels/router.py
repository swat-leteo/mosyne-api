"""
Router - Angel routes.
"""

# Typings
from typing import List
from uuid import UUID

# Responses
from api.utils import responses
from api.utils.responses import create_responses

# Security utils
from api.utils.security import get_auth_user

# FastAPI
from fastapi import APIRouter, Depends, Query

# Controller
from .controller import (
    create_angel,
    delete_angel,
    get_angel,
    get_angels_of_user,
    get_qr_code,
    update_angel,
    update_angel_contact,
)

# schemas
from .schema import (
    AngelCreateDto,
    AngelDto,
    AngelListDto,
    AngelQrDto,
    AngelUpdateDto,
    ContactDto,
)

################
# Angel router #
################

router = APIRouter()


@router.post(
    "",
    status_code=201,
    response_model=AngelDto,
    responses=create_responses([400, 401, 403, 412]),
)
async def add_new_angel(
    angel_info: AngelCreateDto,
    contacts: List[ContactDto],
    im_my_guardian: bool = Query(False),
    use_guardian_address: bool = Query(False),
    user=Depends(get_auth_user),
) -> AngelDto:
    """Create a new angel."""
    angel = await create_angel(
        angel_info, contacts, im_my_guardian, use_guardian_address, user
    )
    return angel


@router.get(
    "",
    status_code=200,
    response_model=List[AngelDto],
    responses=create_responses([401, 403]),
)
async def get_all_angels(user=Depends(get_auth_user)) -> AngelListDto:
    """Retrieve all angels of the current user."""
    angels = await get_angels_of_user(user)
    return angels


@router.get(
    "/{id}",
    status_code=200,
    response_model=AngelDto,
    responses=create_responses([401, 403, 404]),
)
async def get_angel_by_ud(id: UUID) -> AngelDto:
    """Retrieve an angel by ID."""
    angel = await get_angel(id)
    return angel


@router.get(
    "/{id}/qr",
    status_code=200,
    response_model=AngelQrDto,
    responses=create_responses([401, 403, 404]),
    dependencies=[Depends(get_auth_user)]
)
async def get_angel_qr_code(id: UUID) -> AngelQrDto:
    """Retrieve the angel QR code image in base64 format."""
    qr_code = await get_qr_code(id)
    return qr_code


@router.put(
    "/{id}",
    status_code=200,
    response_model=AngelDto,
    responses=create_responses([400, 401, 403, 404, 409]),
    dependencies=[Depends(get_auth_user)],
)
async def update_angel_data(id: UUID, angel_info: AngelUpdateDto) -> AngelDto:
    """Update an angel and return its data updated."""
    angel = await update_angel(id, angel_info)
    return angel


@router.put(
    "/contact/{id}",
    status_code=200,
    response_model=AngelDto,
    responses=create_responses([400, 401, 403, 404]),
    dependencies=[Depends(get_auth_user)],
)
async def update_angel_contact_data(id: UUID, contact_info: ContactDto) -> AngelDto:
    """Update an angel contact data and return the angel updated."""
    angel = await update_angel_contact(id, contact_info)
    return angel


@router.delete(
    "/{id}",
    status_code=200,
    response_model=responses.Msg,
    responses=create_responses([401, 403, 404]),
    dependencies=[Depends(get_auth_user)],
)
async def delete_angel_by_id(id: UUID) -> responses.Msg:
    """Delete angel by ID."""
    await delete_angel(id)
    return responses.Msg(detail="Angel deleted")
