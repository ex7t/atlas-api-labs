from fastapi import HTTPException, status

from src.enums.auth import AuthMessage


class InvalidCredentials(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            AuthMessage.INVALID_CREDENTIALS,
            headers={"WWW-Authenticate": "Bearer"},
        )


class InvalidToken(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            AuthMessage.INVALID_TOKEN,
            headers={"WWW-Authenticate": "Bearer"},
        )


class ForbiddenProfile(HTTPException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, AuthMessage.FORBIDDEN)
