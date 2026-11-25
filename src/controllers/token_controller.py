from datetime import UTC, datetime, timedelta

from settings import app_settings
from src.enums.auth import TokenKind
from src.repositories.token_repository import TokenRepository
from src.schemas.auth import TokensResponse
from src.utils.jwt_tokens import encode_token


class TokenController:
    def __init__(self, repository: TokenRepository) -> None:
        self.repository = repository

    async def issue(self, user_id: int) -> TokensResponse:
        now = datetime.now(UTC).replace(microsecond=0)
        refresh_until = now + timedelta(days=app_settings.REFRESH_TOKEN_DAYS)
        access_until = min(
            refresh_until, now + timedelta(minutes=app_settings.ACCESS_TOKEN_MINUTES)
        )
        await self.repository.delete_expired_tokens(user_id, now)
        refresh = await self.repository.create_refresh(user_id, now, refresh_until)
        access = await self.repository.create_access(refresh, access_until)
        return TokensResponse(
            access_token=encode_token(access, TokenKind.ACCESS),
            refresh_token=encode_token(refresh, TokenKind.REFRESH),
        )
