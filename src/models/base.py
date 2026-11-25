from datetime import datetime

from sqlalchemy import DateTime, false
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class AutoIdMixin:
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class SoftDeleteMixin:
    is_deleted: Mapped[bool] = mapped_column(default=False, server_default=false())
    deleted_by: Mapped[int | None]
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class CrudModel(AutoIdMixin, SoftDeleteMixin, Base):
    __abstract__ = True
