from sqlalchemy.ext.asyncio import AsyncSession

from src.models import PostModel
from src.schemas.posts import PostFullDto, PostWrite

from .base_db_repository import BaseDbRepository


class PostRepository(BaseDbRepository[PostModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, PostModel)

    async def list(self) -> list[PostFullDto]:
        return [PostFullDto.model_validate(row) for row in await self.list_rows()]

    async def get(self, post_id: int) -> PostFullDto | None:
        row = await self.get_row(post_id)
        return PostFullDto.model_validate(row) if row is not None else None

    async def create(self, data: PostWrite) -> PostFullDto:
        row = await self.upsert(data.model_dump())
        result = PostFullDto.model_validate(row)
        await self.session.commit()
        return result

    async def update(self, post_id: int, data: PostWrite) -> PostFullDto | None:
        row = await self.update_row(post_id, data.model_dump())
        result = PostFullDto.model_validate(row) if row is not None else None
        await self.session.commit()
        return result

    async def delete(self, post_id: int) -> bool:
        deleted = await self.delete_row(post_id)
        await self.session.commit()
        return deleted
