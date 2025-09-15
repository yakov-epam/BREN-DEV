from typing import AsyncGenerator

from fastapi import Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from db.repositories.generic import GenericRepository
from db.models import users as models
from db.schemas import users as schemas
from generic_deps import get_db_session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRepository(
    GenericRepository[models.User, schemas.User, schemas.UserCreate, schemas.UserUpdate]
):
    async def create_one(self, data: schemas.UserCreate) -> schemas.User:
        """
        Create one user.
        :param data: User to create.
        :return: Created user.
        """
        data.password = pwd_context.hash(data.password)
        return await super().create_one(data)


async def get_repo(
    session: Session = Depends(get_db_session),
) -> AsyncGenerator[UserRepository]:
    """
    User repository FastAPI dependency.
    :param session: Database session.
    :return: New user repository instance.
    """
    yield UserRepository(session, models.User, schemas.User)
