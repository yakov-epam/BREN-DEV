from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.orm import Session

from db.models import books as models
from db.schemas import books as schemas
from db.repositories.generic import GenericRepository
from generic_deps import get_db_session


class BookRepository(
    GenericRepository[models.Book, schemas.Book, schemas.BookCreate, schemas.BookUpdate]
):
    pass


async def get_repo(
    session: Session = Depends(get_db_session),
) -> AsyncGenerator[BookRepository]:
    """
    Book repository dependency.
    :param session: Database session.
    :return: New book repository instance.
    """
    yield BookRepository(session, models.Book, schemas.Book)
