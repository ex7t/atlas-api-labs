from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column

from settings import app_settings

from .base import AutoIdMixin, Base
from .user_model import UserModel

schema = app_settings.USERS_SQL_SCHEMA


class TokenModel(AutoIdMixin, Base):
    __abstract__ = True

    user_id: Mapped[int] = mapped_column(ForeignKey(UserModel.id, ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    expire_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class RefreshTokenModel(TokenModel):
    __tablename__ = "refresh_token"
    __table_args__ = (
        Index("ix_refresh_token_user", "user_id"),
        {"schema": schema},
    )


class AccessTokenModel(TokenModel):
    __tablename__ = "access_token"
    __table_args__ = {"schema": schema}

    refresh_id: Mapped[int] = mapped_column(
        ForeignKey(RefreshTokenModel.id, ondelete="CASCADE"), unique=True
    )
