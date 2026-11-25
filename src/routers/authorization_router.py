from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import SecretStr

from src.controllers.authorization_controller import AuthorizationController
from src.controllers.user_controller import UserController
from src.dependencies.auth import get_authorization_controller
from src.dependencies.users import get_user_controller
from src.schemas.auth import LoginRequest, TokensResponse
from src.schemas.users import UserFullDto, UserWrite

router = APIRouter(prefix="/authorization", tags=["Авторизация"])
LoginController = Annotated[AuthorizationController, Depends(get_authorization_controller)]
AccountController = Annotated[UserController, Depends(get_user_controller)]


@router.post("/register", status_code=status.HTTP_201_CREATED, summary="Зарегистрироваться")
async def register(data: UserWrite, controller: AccountController) -> UserFullDto:
    return await controller.create(data)


@router.post("/login", summary="Войти и получить пару JWT")
async def login(data: LoginRequest, controller: LoginController) -> TokensResponse:
    return await controller.login(data.login, data.password)


@router.post("/token", response_model_by_alias=False, summary="Получить токены через OAuth2")
async def token(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    controller: LoginController,
) -> TokensResponse:
    return await controller.login(form.username, SecretStr(form.password))
