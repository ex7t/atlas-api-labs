from typing import Annotated

from fastapi import APIRouter, Depends

from src.controllers.authentication_controller import AuthenticationController
from src.dependencies.auth import get_authentication_controller
from src.schemas.auth import (
    LogoutResponse,
    RefreshTokenRequest,
    TokensResponse,
    VerifyAccessTokenRequest,
    VerifyAccessTokenResponse,
)

router = APIRouter(prefix="/authentication", tags=["Аутентификация"])
Controller = Annotated[AuthenticationController, Depends(get_authentication_controller)]


@router.post("/verify_access_token", summary="Проверить access-токен")
async def verify(
    data: VerifyAccessTokenRequest, controller: Controller
) -> VerifyAccessTokenResponse:
    return await controller.verify(data.access_token)


@router.post("/refresh_tokens", summary="Обновить пару токенов")
async def refresh(data: RefreshTokenRequest, controller: Controller) -> TokensResponse:
    return await controller.refresh(data.refresh_token)


@router.post("/logout", summary="Завершить сеанс")
async def logout(data: RefreshTokenRequest, controller: Controller) -> LogoutResponse:
    return await controller.logout(data.refresh_token)
