from typing import Annotated

from fastapi import Depends

from src.controllers.post_controller import PostController
from src.repositories.post_repository import PostRepository

post_repository = PostRepository()


async def get_post_repository() -> PostRepository:
    return post_repository


async def get_post_controller(
    repository: Annotated[PostRepository, Depends(get_post_repository)],
) -> PostController:
    return PostController(repository)
