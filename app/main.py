"""
Main app entry point.
"""

# App
from api import api_router
from config import settings
from db import TORTOISE_ORM_CONFIG

# FastAPI
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

# Tortoise ORM
from tortoise.contrib.fastapi import register_tortoise

################
# App Settings #
################

app = FastAPI(
    title=settings.APP_NAME,
    description="",
    version="1.0",
)


###############
# DB Settings #
###############

register_tortoise(app, config=TORTOISE_ORM_CONFIG, generate_schemas=False)


###############
# Middlewares #
###############

# CORS middleware
if len(settings.CORS_ORIGIN) != 0:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGIN,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Session middleware (needed to implements google auth)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_JWT)

##########
# Router #
##########

app.include_router(api_router, prefix="/api")
