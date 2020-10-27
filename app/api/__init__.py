"""
Main API - Router
"""

# Routers
from api.auth.router import router as auth_router
from api.users.router import router as user_router
from api.angels.router import router as angel_router

# FastApi
from fastapi import APIRouter

################
# API - ROUTER #
################

api_router = APIRouter()

# --- AUTH router --- #
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])

# --- USER router --- #
api_router.include_router(user_router, prefix="/user", tags=["Users"])

# --- ANGEL router --- #
api_router.include_router(angel_router, prefix="/angel", tags=["Angels"])
