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
    """
    Create a new user in the database.
    :param role: User role.
    :return: Created user schema.
    """
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
async def create_user_user() -> User:
    """
    Create a new user with role "user" in the database.
    :return: Created user schema.
    """
    return await create_user(enums.UserRole.USER)


@asynccontextmanager
async def create_client(token: str | None) -> AsyncGenerator[httpx.AsyncClient]:
    """
    Create a new HTTP client.
    :param token: Optional JWT token to use for auth.
    :return: HTTP client instance.
    """
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
    """
    HTTP client fixture, authorized as a user with "user" role.
    Use this to make requests.
    :param http_client: HTTP client instance.
    :return: HTTP client instance.
    """
    item = await create_user(role=enums.UserRole.USER)
    token = create_access_token({"sub": str(item.id)})
    async with create_client(token) as client:
        yield client


@pytest.fixture(scope="function")
async def admin_http_client(
    http_client: httpx.AsyncClient,
) -> AsyncGenerator[httpx.AsyncClient]:
    """
    HTTP client fixture, authorized as a user with "admin" role.
    Use this to make requests.
    :param http_client: HTTP client instance.
    :return: HTTP client instance.
    """
    item = await create_user(role=enums.UserRole.ADMIN)
    token = create_access_token({"sub": str(item.id)})
    async with create_client(token) as client:
        yield client


@pytest.fixture(scope="function")
async def client(
    request, http_client, user_http_client, admin_http_client
) -> AsyncGenerator[httpx.AsyncClient]:
    """
    Dynamic HTTP client fixture,
    determining target user role based on passed param.
    :param request: Pytest request object.
    :param http_client: HTTP client instance.
    :param user_http_client: HTTP client instance.
    :param admin_http_client: HTTP client instance.
    :return: HTTP client instance.
    :raise: ValueError if provided user role is invalid.
    """
    if request.param is None:
        yield http_client
    elif request.param == enums.UserRole.ADMIN:
        yield admin_http_client
    elif request.param == enums.UserRole.USER:
        yield user_http_client
    else:
        raise ValueError(f"Invalid role: {request.param}")
