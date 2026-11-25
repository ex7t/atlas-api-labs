from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.controllers.authentication_controller import AuthenticationController
from src.controllers.authorization_controller import AuthorizationController
from src.controllers.token_controller import TokenController
from src.repositories.user_repository import UserRepository

from .tokens import TokenRepo, get_token_controller
from .users import get_user_repository

UserRepo = Annotated[UserRepository, Depends(get_user_repository)]
Tokens = Annotated[TokenController, Depends(get_token_controller)]
bearer = OAuth2PasswordBearer(tokenUrl="authorization/token")


async def get_authorization_controller(users: UserRepo, tokens: Tokens) -> AuthorizationController:
    return AuthorizationController(users, tokens)


async def get_authentication_controller(
    repository: TokenRepo, users: UserRepo, tokens: Tokens
) -> AuthenticationController:
    return AuthenticationController(repository, users, tokens)


async def get_current_user_id(
    access_token: Annotated[str, Depends(bearer)],
    controller: Annotated[AuthenticationController, Depends(get_authentication_controller)],
) -> int:
    return await controller.get_user_id(access_token)


CurrentUserId = Annotated[int, Depends(get_current_user_id)]
