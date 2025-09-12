"""seed_books

Revision ID: dc8aaa190a6f
Revises: 6327879f1d79
Create Date: 2025-09-11 16:02:14.001711

"""

from typing import Sequence, Union
from sqlalchemy import table, column, String, Integer, Float
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "dc8aaa190a6f"
down_revision: Union[str, Sequence[str], None] = "c77820223ed5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = "c77820223ed5"


books_table = table(
    "books",
    column("id", Integer),
    column("title", String),
    column("author", String),
    column("pages", Integer),
    column("rating", Float),
    column("price", Float),
)


def upgrade() -> None:
    """Upgrade schema."""
    op.bulk_insert(
        books_table,
        rows=[
            {
                "title": "To Kill a Mockingbird",
                "author": "Harper Lee",
                "pages": 324,
                "rating": 4.8,
                "price": 14.99,
            },
            {
                "title": "1984",
                "author": "George Orwell ",
                "pages": 328,
                "rating": 4.7,
                "price": 12.95,
            },
            {
                "title": "Animal Farm",
                "author": "George Orwell ",
                "pages": 112,
                "rating": 4.6,
                "price": 8.99,
            },
            {
                "title": "Pride and Prejudice",
                "author": "Jane Austen",
                "pages": 279,
                "rating": 4.6,
                "price": 9.99,
            },
            {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "pages": 180,
                "rating": 4.4,
                "price": 10.99,
            },
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
