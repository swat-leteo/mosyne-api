"""
Router - Angel routes.
"""

# Responses
from api.utils import responses
from api.utils.responses import create_responses

# Security utils
from api.utils.security import get_auth_user

# FastAPI
from fastapi import APIRouter, Depends, Query

###############
# User router #
###############

router = APIRouter()
