from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from settings import app_settings

engine = create_async_engine(
    app_settings.database_url, echo=app_settings.SQL_ECHO, hide_parameters=True, pool_pre_ping=True
)
sessions = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with sessions() as session:
        yield session


DbSession = Annotated[AsyncSession, Depends(get_session)]
