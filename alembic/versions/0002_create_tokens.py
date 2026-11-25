"""Create refresh and access token tables."""

import sqlalchemy as sa
from alembic import op

from settings import app_settings

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def token_columns(schema: str) -> tuple[sa.Column, ...]:
    return (
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey(f"{schema}.user.id", ondelete="CASCADE"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expire_at", sa.DateTime(timezone=True), nullable=False),
    )


def upgrade() -> None:
    schema = app_settings.USERS_SQL_SCHEMA
    op.create_table("refresh_token", *token_columns(schema), schema=schema)
    op.create_index("ix_refresh_token_user", "refresh_token", ["user_id"], schema=schema)
    op.create_table(
        "access_token",
        *token_columns(schema),
        sa.Column(
            "refresh_id",
            sa.Integer(),
            sa.ForeignKey(f"{schema}.refresh_token.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        schema=schema,
    )


def downgrade() -> None:
    schema = app_settings.USERS_SQL_SCHEMA
    op.drop_table("access_token", schema=schema)
    op.drop_table("refresh_token", schema=schema)
