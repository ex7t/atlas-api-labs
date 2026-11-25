from datetime import UTC, datetime
from typing import Any, Generic, TypeVar

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.base import CrudModel


Model = TypeVar("Model", bound=CrudModel)


class BaseDbRepository(Generic[Model]):
    def __init__(self, session: AsyncSession, model: type[Model]) -> None:
        self.session = session
        self.model = model

    async def list_rows(self) -> list[Model]:
        query = select(self.model).where(self.model.is_deleted.is_(False)).order_by(self.model.id)
        return list((await self.session.scalars(query)).all())

    async def get_row(self, object_id: int, *, lock: bool = False) -> Model | None:
        query = select(self.model).where(
            self.model.id == object_id, self.model.is_deleted.is_(False)
        )
        if lock:
            query = query.with_for_update()
        return await self.session.scalar(query)

    async def upsert(self, values: dict[str, Any]) -> Model | None:
        statement = insert(self.model).values(values)
        changes = {key: statement.excluded[key] for key in values if key != "id"}
        statement = statement.on_conflict_do_update(
            index_elements=[self.model.id],
            set_=changes,
            where=self.model.is_deleted.is_(False),
        ).returning(self.model)
        return await self.session.scalar(statement, execution_options={"populate_existing": True})

    async def update_row(self, object_id: int, values: dict[str, Any]) -> Model | None:
        statement = (
            update(self.model)
            .where(self.model.id == object_id, self.model.is_deleted.is_(False))
            .values(values)
            .returning(self.model)
        )
        return await self.session.scalar(statement)

    async def delete_row(self, object_id: int, *, actor_id: int | None = None) -> bool:
        row = await self.update_row(
            object_id,
            {"is_deleted": True, "deleted_at": datetime.now(UTC), "deleted_by": actor_id},
        )
        return row is not None
