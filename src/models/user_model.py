from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from settings import app_settings

from .base import CrudModel


class UserModel(CrudModel):
    __tablename__ = "user"
    __table_args__ = {"schema": app_settings.USERS_SQL_SCHEMA}

    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(120), unique=True)
    login: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255))
