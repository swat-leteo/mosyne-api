"""
Main API - Router
"""

# Routers
from api.angels.router import router as angel_router
from api.auth.router import router as auth_router
from api.users.router import router as user_router

# FastApi
from fastapi import APIRouter

################
# API - ROUTER #
################

api_router = APIRouter()

# --- AUTH router --- #
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])

# --- USER router --- #
api_router.include_router(user_router, prefix="/users", tags=["Users"])

# --- ANGEL router --- #
api_router.include_router(angel_router, prefix="/angels", tags=["Angels"])
