from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import UserModel

from .base_db_repository import BaseDbRepository


class UserRepository(BaseDbRepository[UserModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, UserModel)

    async def get_by_login(self, login: str) -> UserModel | None:
        query = select(UserModel).where(
            UserModel.login == login, UserModel.is_deleted.is_(False)
        ).with_for_update()
        return await self.session.scalar(query)
