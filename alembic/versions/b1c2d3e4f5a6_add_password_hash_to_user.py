"""add password_hash to user

Revision ID: b1c2d3e4f5a6
Revises: 9cb20ca7a2e0
Create Date: 2026-11-26 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b1c2d3e4f5a6"
down_revision: Union[str, Sequence[str], None] = "9cb20ca7a2e0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "user",
        sa.Column("password_hash", sa.String(), nullable=False, server_default=""),
    )
    op.alter_column("user", "password_hash", server_default=None)


def downgrade() -> None:
    op.drop_column("user", "password_hash")
