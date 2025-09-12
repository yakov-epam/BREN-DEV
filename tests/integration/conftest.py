from typing import AsyncGenerator, Generator
from const import DATABASE
from main import create_app
from contextlib import asynccontextmanager
import pytest
import httpx
from alembic import command
from alembic.config import Config
from db.models.users import User as UserModel
from db.schemas.users import User
from db import enums
from uuid import uuid4

from v1.security import create_access_token

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


async def create_user(role: enums.UserRole) -> User:
    with DATABASE.session_maker() as session:
        item = UserModel(
            username=uuid4().hex,
            # testtest
            password="$2b$12$oPkNubVyRG5rpn.2W.3ky.wDtg2JOJEFcDL4fe1kVwpHFdCpuNuw.",
            role=role,
        )
        session.add(item)
        session.commit()
        session.refresh(item)
    return item


@pytest.fixture(scope="function")
async def create_user_user():
    return await create_user(enums.UserRole.USER)


@asynccontextmanager
async def create_client(token: str | None) -> AsyncGenerator[httpx.AsyncClient]:
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(APP),
        base_url="http://test/v1",
        headers=headers,
        timeout=5,
    ) as client:
        yield client


@pytest.fixture(scope="function")
async def http_client() -> AsyncGenerator[httpx.AsyncClient]:
    """
    HTTP client fixture. Use this to make requests.
    :return: HTTP client instance.
    """
    async with create_client(None) as client:
        yield client


@pytest.fixture(scope="function")
async def user_http_client(
    http_client: httpx.AsyncClient,
) -> AsyncGenerator[httpx.AsyncClient]:
    item = await create_user(role=enums.UserRole.USER)
    token = create_access_token({"sub": str(item.id)})
    async with create_client(token) as client:
        yield client


@pytest.fixture(scope="function")
async def admin_http_client(
    http_client: httpx.AsyncClient,
) -> AsyncGenerator[httpx.AsyncClient]:
    item = await create_user(role=enums.UserRole.ADMIN)
    token = create_access_token({"sub": str(item.id)})
    async with create_client(token) as client:
        yield client


@pytest.fixture(scope="function")
async def client(request, http_client, user_http_client, admin_http_client):
    if request.param is None:
        yield http_client
    elif request.param == enums.UserRole.ADMIN:
        yield admin_http_client
    elif request.param == enums.UserRole.USER:
        yield user_http_client
    else:
        raise ValueError(f"Invalid role: {request.param}")
