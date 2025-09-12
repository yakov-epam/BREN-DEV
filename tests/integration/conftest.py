from typing import AsyncGenerator, Generator
from const import DATABASE
from main import create_app
import pytest
import httpx
from alembic import command
from alembic.config import Config
from db.models.books import Book

APP = create_app()


@pytest.fixture(scope="session", autouse=True)
def setup_database() -> Generator[None]:
    """
    Database setup and teardown.
    :return: None.
    """
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    yield


@pytest.fixture(scope="function")
async def http_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    """
    HTTP client fixture. Use this to make requests.
    :return: HTTP client instance.
    """
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(APP),
        base_url="http://test/v1",
        headers={"Content-Type": "application/json"},
        timeout=5,
    ) as client:
        yield client


@pytest.fixture(scope="function")
async def create_book() -> AsyncGenerator[Book, None]:
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
