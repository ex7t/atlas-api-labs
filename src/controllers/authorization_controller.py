from pydantic import SecretStr

from src.controllers.token_controller import TokenController
from src.exceptions.auth import InvalidCredentials
from src.repositories.user_repository import UserRepository
from src.schemas.auth import TokensResponse
from src.utils.passwords import DUMMY_HASH, verify_password


class AuthorizationController:
    def __init__(self, users: UserRepository, tokens: TokenController) -> None:
        self._users = users
        self._tokens = tokens

    async def login(self, login: str, password: SecretStr) -> TokensResponse:
        user = await self._users.get_by_login(login)
        matches = await verify_password(password, user.password if user is not None else DUMMY_HASH)
        if user is None or not matches:
            raise InvalidCredentials()
        result = await self._tokens.issue(user.id)
        await self._users.session.commit()
        return result
