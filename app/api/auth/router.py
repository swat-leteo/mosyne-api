"""
Router - Auth routes.
"""

# Calling the User models to instance and handle user info

from api.utils import responses
from fastapi import Response
from fastApi import ApiRouter, BackgroundTask
from services.mails import send_verification_email
from users.schema import UserDto
from utils.security import create_access_token, set_credential

from .controller import login, signup
from .schema import LoginCredentials, SignupInfo

router = ApiRouter()


@router.post("/signup")
async def register_user(user_info: SignupInfo, background_task: BackgroundTask):
    """
    Signup route

    Params:
    -------
    - user_info: SignupInfo - the user registration information
    - background_task: BackgroundTask - ?????
    """
    user = await signup(user_info)
    verification_token = create_access_token(user.email, True)
    background_task.add_task(
        send_verification_email,
        recipient_name=user.firstname,
        email=user.email,
        token=verification_token,
    )
    return responses.EmailMsg("Email sent")

@router.post("/login")
async def authenticate_user(
    credentials: LoginCredentials, response: Response
) -> UserDto:
    user = await login(credentials)
    token = create_access_token(user.email)
    set_credential(response, token)
    return user
