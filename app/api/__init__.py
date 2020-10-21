"""
Main API - Router
"""

from fastapi import APIRouter
from api.users.router import router as user_router

################
# API - ROUTER #
################

api_router = APIRouter()

# --- AUTH router --- #
# api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])


# --- AUTH router --- #
api_router.include_router(user_router, prefix="/user", tags=["User"])
