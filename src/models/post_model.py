from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from settings import app_settings

from .base import CrudModel


class PostModel(CrudModel):
    __tablename__ = "post"
    __table_args__ = {"schema": app_settings.POSTS_SQL_SCHEMA}

    name: Mapped[str] = mapped_column(String(255))
    author_name: Mapped[str] = mapped_column(String(50))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
