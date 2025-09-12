from const import DATABASE
from sqlalchemy.orm import Session
from typing import AsyncGenerator


async def get_db_session() -> AsyncGenerator[Session]:
    """
    Database session dependency.
    :return: New database session.
    """
    async with DATABASE.session() as session:
        yield session
