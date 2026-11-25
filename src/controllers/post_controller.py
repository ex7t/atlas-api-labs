from fastapi import HTTPException, status

from src.interfaces.posts import PostStore
from src.schemas.posts import PostFullDto, PostWrite


class PostController:
    def __init__(self, repository: PostStore) -> None:
        self._repository = repository

    async def list(self) -> list[PostFullDto]:
        return await self._repository.list()

    async def get(self, post_id: int) -> PostFullDto:
        return self._require_post(await self._repository.get(post_id))

    async def create(self, data: PostWrite) -> PostFullDto:
        return await self._repository.create(data)

    async def update(self, post_id: int, data: PostWrite) -> PostFullDto:
        return self._require_post(await self._repository.update(post_id, data))

    async def delete(self, post_id: int) -> None:
        if not await self._repository.delete(post_id):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Пост не найден")

    @staticmethod
    def _require_post(post: PostFullDto | None) -> PostFullDto:
        if post is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Пост не найден")
        return post
