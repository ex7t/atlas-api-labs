from datetime import datetime

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import AccessTokenModel, RefreshTokenModel, UserModel
from src.schemas.auth import AccessTokenFullDto, RefreshTokenFullDto, TokenDto


class TokenRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_refresh(
        self, user_id: int, created_at: datetime, expire_at: datetime
    ) -> RefreshTokenFullDto:
        row = RefreshTokenModel(user_id=user_id, created_at=created_at, expire_at=expire_at)
        self.session.add(row)
        await self.session.flush()
        return RefreshTokenFullDto.model_validate(row)

    async def create_access(
        self, refresh: RefreshTokenFullDto, expire_at: datetime
    ) -> AccessTokenFullDto:
        row = AccessTokenModel(
            user_id=refresh.user_id, refresh_id=refresh.id,
            created_at=refresh.created_at, expire_at=expire_at,
        )
        self.session.add(row)
        await self.session.flush()
        return AccessTokenFullDto.model_validate(row)

    async def has_access(self, token: TokenDto, now: datetime) -> bool:
        query = (
            select(AccessTokenModel.id)
            .join(RefreshTokenModel, AccessTokenModel.refresh_id == RefreshTokenModel.id)
            .join(UserModel, AccessTokenModel.user_id == UserModel.id)
            .where(
                AccessTokenModel.id == token.id,
                AccessTokenModel.user_id == token.user_id,
                AccessTokenModel.expire_at > now,
                RefreshTokenModel.expire_at > now,
                UserModel.is_deleted.is_(False),
            )
        )
        return await self.session.scalar(query) is not None

    async def consume_refresh(self, token: TokenDto, now: datetime) -> bool:
        statement = (
            delete(RefreshTokenModel)
            .where(
                RefreshTokenModel.id == token.id,
                RefreshTokenModel.user_id == token.user_id,
                RefreshTokenModel.expire_at > now,
            )
            .returning(RefreshTokenModel.id)
        )
        return await self.session.scalar(statement) is not None

    async def delete_expired_tokens(self, user_id: int, now: datetime) -> None:
        await self.session.execute(
            delete(RefreshTokenModel).where(
                RefreshTokenModel.user_id == user_id, RefreshTokenModel.expire_at <= now
            )
        )

    async def revoke_user_tokens(self, user_id: int) -> None:
        await self.session.execute(
            delete(RefreshTokenModel).where(RefreshTokenModel.user_id == user_id)
        )
