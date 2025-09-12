from sqlalchemy import MetaData, Column, Integer
from sqlalchemy.orm import declarative_base


Base = declarative_base(metadata=MetaData(schema="public"))


class BaseDBModelMixin:
    id = Column(Integer, primary_key=True, nullable=False)
