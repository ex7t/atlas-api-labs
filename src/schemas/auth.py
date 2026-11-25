from datetime import datetime
from typing import Annotated, Literal

from pydantic import Field, SecretStr

from src.enums.auth import RegexEnum

from .common import BaseSchema
from .users import Login

JwtString = Annotated[str, Field(pattern=RegexEnum.JWT.value, max_length=4096)]


class LoginRequest(BaseSchema):
    login: Login
    password: SecretStr


class RefreshTokenRequest(BaseSchema):
    refresh_token: JwtString


class VerifyAccessTokenRequest(BaseSchema):
    access_token: JwtString


class TokensResponse(BaseSchema):
    access_token: str
    refresh_token: str
    token_type: Literal["bearer"] = "bearer"


class VerifyAccessTokenResponse(BaseSchema):
    access_token: str


class LogoutResponse(BaseSchema):
    message: str = "Сеанс завершён"


class TokenDto(BaseSchema):
    id: int
    user_id: int
    created_at: datetime
    expire_at: datetime


class RefreshTokenFullDto(TokenDto):
    pass


class AccessTokenFullDto(TokenDto):
    refresh_id: int
