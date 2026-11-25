from typing import Annotated

from fastapi import Depends

from src.controllers.user_controller import UserController
from src.repositories.user_repository import UserRepository

from .database import DbSession


async def get_user_repository(session: DbSession) -> UserRepository:
    return UserRepository(session)


async def get_user_controller(
    repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserController:
    return UserController(repository)
