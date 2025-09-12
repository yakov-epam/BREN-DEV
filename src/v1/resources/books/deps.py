from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.orm import Session

from db.repositories.books import BookRepository
from generic_deps import get_db_session


async def get_repo(
    session: Session = Depends(get_db_session),
) -> AsyncGenerator[BookRepository, None]:
    """
    Books repository dependency.
    :param session: Database session.
    :return: New books repository instance.
    """
    yield BookRepository(session=session)
