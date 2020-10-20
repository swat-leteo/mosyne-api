"""
Custom HTTP exceptions.
"""

# FastAPI
from fastapi import HTTPException, status


def bad_request_400(detail: str) -> None:
    """Raise a 400 http error - BadRequest.

    Params:
    -------
    - detail: str - The exception message.
    """
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


def unauthorized_401() -> None:
    """Raise a 401 http error - Unauthorized."""
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
    )


def forbidden_403() -> None:
    """Raise a 403 http error - Forbidden."""
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")


def not_found_404(detail: str) -> None:
    """Raise a 404 http error - Not Found.

    Params:
    -------
    - detail: str - The exception message.
    """
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


def conflict_409(detail: str) -> None:
    """Raise a 409 http error - Conlict.

    Params:
    -------
    - detail: str - The exception message.
    """
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)
