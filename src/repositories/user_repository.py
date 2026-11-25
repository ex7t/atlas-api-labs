from sqlalchemy.ext.asyncio import AsyncSession

from src.models import UserModel

from .base_db_repository import BaseDbRepository


class UserRepository(BaseDbRepository[UserModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, UserModel)
