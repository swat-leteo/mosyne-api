"""
Main API - Router
"""

from api.users.router import router as user_router
from fastapi import APIRouter

################
# API - ROUTER #
################

api_router = APIRouter()

# --- AUTH router --- #
# api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])

# --- AUTH router --- #
api_router.include_router(user_router, prefix="/user", tags=["User"])
