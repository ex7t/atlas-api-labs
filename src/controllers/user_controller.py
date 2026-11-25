from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from src.models import UserModel
from src.repositories.user_repository import UserRepository
from src.schemas.users import UserFullDto, UserWrite
from src.utils.passwords import hash_password


class UserController:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def list(self) -> list[UserFullDto]:
        return [UserFullDto.model_validate(row) for row in await self.repository.list_rows()]

    async def get(self, user_id: int) -> UserFullDto:
        return self._require_user(await self.repository.get_row(user_id))

    async def create(self, data: UserWrite) -> UserFullDto:
        values = await self._user_values(data)
        try:
            result = UserFullDto.model_validate(await self.repository.upsert(values))
            await self.repository.session.commit()
        except IntegrityError as exc:
            await self.repository.session.rollback()
            raise self._on_conflict() from exc
        return result

    async def update(self, user_id: int, data: UserWrite) -> UserFullDto:
        values = await self._user_values(data)
        try:
            result = self._require_user(await self.repository.update_row(user_id, values))
            await self.repository.session.commit()
        except IntegrityError as exc:
            await self.repository.session.rollback()
            raise self._on_conflict() from exc
        return result

    async def delete(self, user_id: int) -> None:
        if not await self.repository.delete_row(user_id):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Пользователь не найден")
        await self.repository.session.commit()

    @staticmethod
    async def _user_values(data: UserWrite) -> dict[str, Any]:
        values = data.model_dump(exclude={"password"})
        values["password"] = await hash_password(data.password)
        return values

    @staticmethod
    def _require_user(row: UserModel | None) -> UserFullDto:
        if row is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Пользователь не найден")
        return UserFullDto.model_validate(row)

    @staticmethod
    def _on_conflict() -> HTTPException:
        return HTTPException(
            status.HTTP_409_CONFLICT, "Никнейм, логин или почта уже используются"
        )
