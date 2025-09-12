"""Seed users

Revision ID: a3e2c1169c50
Revises: 29435342b3f0
Create Date: 2025-09-12 15:54:45.709434

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import os


# revision identifiers, used by Alembic.
revision: str = "a3e2c1169c50"
down_revision: Union[str, Sequence[str], None] = "29435342b3f0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = "29435342b3f0"

users_table = sa.table(
    "users",
    sa.column("id", sa.Integer),
    sa.column("username", sa.String),
    sa.column("email", sa.String),
    sa.column("password", sa.String),
    sa.column("role", sa.Enum("USER", "ADMIN")),
)


def upgrade() -> None:
    """Upgrade schema."""
    if os.getenv("ENV") != "prod":  # Non-prod only
        op.bulk_insert(
            users_table,
            rows=[
                {
                    "username": "user",
                    "email": "user@example.com",
                    # useruser
                    "password": "$2b$12$uFLNoz2fojJW0QXae3ZIh.HNFbO5NZEiKXBCu0r9jmFA8wzMsTVQu",
                    "role": "USER",
                },
                {
                    "username": "admin",
                    "email": "admin@example.com",
                    # adminadmin
                    "password": "$2b$12$47ugVC.KR2xeDW9wtYe1vOz2lnON71fU7Bxm5WNQmacDGwfeiWH86",
                    "role": "ADMIN",
                },
            ],
        )


def downgrade() -> None:
    """Downgrade schema."""
    pass
