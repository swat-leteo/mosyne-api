"""
Security api utils.
"""

# Built int
from datetime import datetime, timedelta

# DB model
from api.users.models import User

# Settings
from config import settings

# FastAPI
from fastapi import Depends, Response
from fastapi.security.api_key import APIKeyCookie

# Security
from jose import JWTError, jwt
from passlib.context import CryptContext

# Exceptions
from .exceptions import unauthorized_401

#################
# Auth Settings #
#################

SECRET = settings.SECRET_JWT
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30  # One month

######################
# Security Instances #
######################

pwd_context = CryptContext(schemes=["bcrypt"])
auth_scheme = APIKeyCookie(name=settings.COOKIE_SESSION_NAME)


##########################
#  Helper Auth Functions #
##########################


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify the enter password with the hashed password stored in db.

    Params:
    -------
    - plain_password: str - The plain password from the request form.
    - hashed_password: str -The hashed password stored in db.

    Return:
    -------
    - Boolean: True if correct password, False if not.
    """
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(plain_password: str) -> str:
    """Generate a hash of the current password.

    Params:
    -------
    - plain_password: str - The plain password from the request form.

    Return:
    -------
    - hashed_password: str - The password hashed.
    """
    return pwd_context.hash(plain_password)


def create_access_token(email: str, short_duration: bool = False) -> str:
    """Return a encoded jwt.

    Params:
    -------
    - data: dict - The data to encoded in jwt paayload.
    - short_duration: bool - Indicate if the token has a short time duration.

    Return:
    -------
    - encode_jwt: bytes - The encoded json web token.
    """
    to_encode = {"email": email}

    if short_duration:
        expires_delta = timedelta(minutes=25)
    else:
        expires_delta = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)

    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)


def get_from_token(token: str) -> str:
    """Verify the token and return the email in payload if is valid.

    Params:
    -------
    - token: str - The encoded JWT

    Return:
    -------
    - email: str - The user email
    """
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        email = payload["email"]
    except (JWTError, KeyError):
        return unauthorized_401()
    return email


#############################
# Authentication Middleware #
#############################


async def get_auth_user(token: str = Depends(auth_scheme)) -> User:
    """Extract the token from cookie and validate if is valid.
    If the token is valid, return the user.

    Params:
    -------
    - taken: str - The jwt in the cookie request.

    Return:
    -------
    - user: User - The user data.
    """
    email = get_from_token(token)
    user = await User.filter(email=email).first()
    if not user:
        return unauthorized_401()
    return user


######################
# Credentials setter #
######################


def set_credential(response: Response, token: str) -> None:
    """Create a response with directives to set the cookie session.

    Params:
    -------
    - response: Response - The fastAPI response instance.
    - token: str - The encoded JWT.
    """
    response.set_cookie(
        key=settings.COOKIE_SESSION_NAME,
        value=token,
        max_age=settings.COOKIE_SESSION_AGE,
        secure=not settings.DEBUG_MODE,
        httponly=True,
    )
