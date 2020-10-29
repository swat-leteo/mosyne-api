"""
Router - Angel routes.
"""

from typing import List

# Responses
from api.utils import responses
# Security utils
from api.utils.security import get_auth_user

# FastAPI
from fastapi import APIRouter, Depends

from .controller import create_angel, get_angel_id, update_angel_info, delete_angel_data

# schemas
from .schema import AngelCreateDto, AngelDto, ContactDto

###############
# User router #
###############

router = APIRouter()


@router.post("")
async def add_new_angel(
    angel_info: AngelCreateDto, contacts: List[ContactDto], user=Depends(get_auth_user)
) -> AngelDto:
    return await create_angel(angel_info, user, contacts)


@router.get("/{id}")
async def angel_id(id:int):
    return get_angel_id(id)


@router.put("/{id}")
async def update_angel(id: int, angel_info: AngelDto) -> AngelDto:
    return update_angel_info(id, angel_info)


@router.delete("/{id}")
async def delete_angel(id: int) -> responses.Msg:
    await delete_angel_data(id)
    return responses.Msg(detail="Angel deleted")
