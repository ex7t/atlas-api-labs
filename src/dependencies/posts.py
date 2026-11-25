from typing import Annotated

from fastapi import Depends

from src.controllers.post_controller import PostController
from src.dependencies.database import DbSession
from src.repositories.post_repository import PostRepository


async def get_post_repository(session: DbSession) -> PostRepository:
    return PostRepository(session)


async def get_post_controller(
    repository: Annotated[PostRepository, Depends(get_post_repository)],
) -> PostController:
    return PostController(repository)
