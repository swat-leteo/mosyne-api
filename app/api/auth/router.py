"""
Router - Auth routes.
"""

# Responses
from api.utils import responses

# Security utils
from api.utils.security import (
    create_access_token,
    get_auth_user,
    remove_credential,
    set_credential,
)

# Settings
from config import settings

# FastAPI
from fastapi import APIRouter, BackgroundTasks, Body, Depends, Query, Response
from fastapi.responses import RedirectResponse

# Mailing
from services.mails import send_recovery_password_email, send_verification_email

# Controller
from .controller import confirm_email, login, reset_password, signup

# Schemas
from .schema import LoginCredentials, SignupInfo, UserDto

###############
# Auth router #
###############

router = APIRouter()


@router.post(
    "/signup",
    status_code=201,
    responses={
        "201": {"model": responses.EmailMsg},
        "409": {"model": responses.Conflict},
    },
)
async def register_user(
    user_info: SignupInfo, background_task: BackgroundTasks
) -> dict:
    """Register a new user."""
    user = await signup(user_info)
    verification_token = create_access_token(user.email, short_duration=True)

    background_task.add_task(
        send_verification_email,
        recipient_name=user.firstname,
        email=user.email,
        token=verification_token,
    )
    return responses.EmailMsg(detail="Email sent")


@router.post(
    "/login",
    status_code=200,
    responses={
        "200": {"model": UserDto},
        "401": {"model": responses.Unauthorized},
        "403": {"model": responses.Forbidden},
        "412": {"model": responses.PreconditionFailed},
    },
)
async def login_user(credentials: LoginCredentials, response: Response) -> UserDto:
    """Verify user credentials and return user info."""
    user = await login(credentials.email, credentials.password)
    session_token = create_access_token(user.email)
    set_credential(response, session_token)
    return user


@router.post(
    "/logout",
    status_code=200,
    responses={
        "200": {"model": responses.Msg},
    },
    dependencies=[Depends(get_auth_user)],
)
async def logout_user(response: Response) -> dict:
    """Remove session cookies."""
    remove_credential(response)
    return responses.Msg(detail="Logout")


@router.post(
    "/verification",
    status_code=200,
    responses={
        "200": {"model": responses.Msg},
    },
)
async def resend_verification_email(
    background_task: BackgroundTasks,
    email: str = Query(...),
) -> dict:
    """Resend a verification email to the current user."""
    verification_token = create_access_token(email=email, short_duration=True)
    background_task.add_task(
        send_verification_email,
        recipient_name="Guardian",
        email=email,
        token=verification_token,
    )
    return responses.Msg(detail="Email sent")


@router.post(
    "/recovery-password",
    status_code=200,
    responses={
        "200": {"model": responses.Msg},
    },
)
async def send_recovery_email(
    background_task: BackgroundTasks,
    email: str = Query(...),
) -> dict:
    """Send a email with recovery password token."""
    verification_token = create_access_token(email=email, short_duration=True)
    background_task.add_task(
        send_recovery_password_email,
        email=email,
        token=verification_token,
    )
    return responses.Msg(detail="Email sent")


@router.post(
    "/reset-password",
    status_code=200,
    responses={
        "200": {"model": responses.Msg},
        "404": {"model": responses.NotFound},
    },
)
async def reset_credentials(
    token: str = Body(...),
    password: str = Body(...),
) -> UserDto:
    """Reset the user password."""
    await reset_password(token, password)
    return responses.Msg(detail="Password reseted")


@router.get(
    "/make-verification",
    status_code=200,
    responses={
        "200": {"model": responses.Msg},
    },
)
async def confirm_user_email(token: str = Query(...)) -> None:
    """Validate the user email address."""
    await confirm_email(token)
    return RedirectResponse(url=f"{settings.WEB_HOST}/login")
