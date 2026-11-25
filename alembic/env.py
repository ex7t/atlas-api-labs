import asyncio

from alembic import context
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from settings import app_settings
from src.models import Base

schemas = {app_settings.USERS_SQL_SCHEMA, app_settings.POSTS_SQL_SCHEMA}


def include_name(name, type_, parent_names):
    return type_ != "schema" or name in schemas


def run_migrations(connection: Connection | None = None) -> None:
    options = {
        "target_metadata": Base.metadata,
        "include_schemas": True,
        "include_name": include_name,
    }
    if connection is None:
        context.configure(url=app_settings.database_url, literal_binds=True, **options)
    else:
        context.configure(connection=connection, **options)

    with context.begin_transaction():
        context.run_migrations()


async def run_online() -> None:
    engine = create_async_engine(app_settings.database_url, poolclass=NullPool)
    try:
        async with engine.connect() as connection:
            await connection.run_sync(run_migrations)
    finally:
        await engine.dispose()


if context.is_offline_mode():
    run_migrations()
else:
    asyncio.run(run_online())
