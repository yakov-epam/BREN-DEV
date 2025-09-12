from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
import contextlib
from typing import AsyncIterator


class DB:
    def __init__(self, host: str, port: int, database: str, user: str, password: str):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.url = self.create_url()
        self.engine = create_engine(
            url=self.url,
            echo=True,
        )
        self.session_maker = sessionmaker(bind=self.engine, autocommit=False)

    def create_url(self) -> str:
        """
        Get current database URL.
        :return: Current database URL.
        """
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[Session]:
        """
        Create a new database session.
        :return: New database session.
        """
        session = self.session_maker()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
