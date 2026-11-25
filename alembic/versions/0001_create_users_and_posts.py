"""Create PostgreSQL schemas, users and posts."""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.schema import CreateSchema

from settings import app_settings

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def soft_delete_columns() -> tuple[sa.Column, ...]:
    return (
        sa.Column("is_deleted", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("deleted_by", sa.Integer()),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
    )


def upgrade() -> None:
    users = app_settings.USERS_SQL_SCHEMA
    posts = app_settings.POSTS_SQL_SCHEMA
    for schema in sorted({users, posts}):
        op.execute(CreateSchema(schema, if_not_exists=True))

    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("username", sa.String(50), nullable=False, unique=True),
        sa.Column("email", sa.String(120), nullable=False, unique=True),
        sa.Column("login", sa.String(255), nullable=False, unique=True),
        sa.Column("password", sa.String(255), nullable=False),
        *soft_delete_columns(),
        schema=users,
    )
    op.create_table(
        "post",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("author_name", sa.String(50), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        *soft_delete_columns(),
        schema=posts,
    )


def downgrade() -> None:
    op.drop_table("post", schema=app_settings.POSTS_SQL_SCHEMA)
    op.drop_table("user", schema=app_settings.USERS_SQL_SCHEMA)
