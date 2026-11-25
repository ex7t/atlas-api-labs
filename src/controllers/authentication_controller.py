from datetime import UTC, datetime

from src.controllers.token_controller import TokenController
from src.enums.auth import TokenKind
from src.exceptions.auth import InvalidToken
from src.repositories.token_repository import TokenRepository
from src.repositories.user_repository import UserRepository
from src.schemas.auth import LogoutResponse, TokensResponse, VerifyAccessTokenResponse
from src.utils.jwt_tokens import decode_token


class AuthenticationController:
    def __init__(
        self, repository: TokenRepository, users: UserRepository, tokens: TokenController
    ) -> None:
        self._repository = repository
        self._users = users
        self._tokens = tokens

    async def get_user_id(self, access_token: str) -> int:
        token = decode_token(access_token, TokenKind.ACCESS)
        if not await self._repository.has_access(token, datetime.now(UTC)):
            raise InvalidToken()
        return token.user_id

    async def verify(self, access_token: str) -> VerifyAccessTokenResponse:
        await self.get_user_id(access_token)
        return VerifyAccessTokenResponse(access_token=access_token)

    async def refresh(self, refresh_token: str) -> TokensResponse:
        token = decode_token(refresh_token, TokenKind.REFRESH)
        user = await self._users.get_row(token.user_id, lock=True)
        if user is None or not await self._repository.consume_refresh(token, datetime.now(UTC)):
            raise InvalidToken()
        result = await self._tokens.issue(token.user_id)
        await self._repository.session.commit()
        return result

    async def logout(self, refresh_token: str) -> LogoutResponse:
        token = decode_token(refresh_token, TokenKind.REFRESH)
        if not await self._repository.consume_refresh(token, datetime.now(UTC)):
            raise InvalidToken()
        await self._repository.session.commit()
        return LogoutResponse()
