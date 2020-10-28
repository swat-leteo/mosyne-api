"""
Router - Angel routes.
"""

from typing import List

# Responses
# Security utils
from api.utils.security import get_auth_user

# FastAPI
from fastapi import APIRouter, Depends

from .controller import create_angel

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
