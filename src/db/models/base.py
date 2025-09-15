from sqlalchemy import MetaData, Column, Integer
from sqlalchemy.orm import declarative_base


Base = declarative_base(metadata=MetaData(schema="public"))


class BaseDBModelMixin:
    """
    Base DB model mixin, defining shared base columns for tables.
    """

    id = Column(Integer, primary_key=True, nullable=False)
