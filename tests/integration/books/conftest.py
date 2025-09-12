import pytest
from db.models.books import Book
from typing import AsyncGenerator
from const import DATABASE


@pytest.fixture(scope="function")
async def create_book() -> AsyncGenerator[Book]:
    """
    Create a book directly in the database.
    Use this for tests that require book presence in the DB to run.
    :return: Book instance.
    """
    with DATABASE.session_maker() as session:
        item = Book(
            title="Test book",
            author="Test author",
            pages=31,
            rating=4.1,
            price=12.53,
        )
        session.add(item)
        session.commit()
        session.refresh(item)
    yield item
