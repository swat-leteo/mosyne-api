"""
Main API - Router
"""

from fastapi import APIRouter

################
# API - ROUTER #
################

api_router = APIRouter()

# --- AUTH router --- #
# api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
