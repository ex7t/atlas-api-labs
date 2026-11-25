from typing import Annotated

from fastapi import Depends

from src.controllers.token_controller import TokenController
from src.repositories.token_repository import TokenRepository

from .database import DbSession


async def get_token_repository(session: DbSession) -> TokenRepository:
    return TokenRepository(session)


TokenRepo = Annotated[TokenRepository, Depends(get_token_repository)]


async def get_token_controller(repository: TokenRepo) -> TokenController:
    return TokenController(repository)
