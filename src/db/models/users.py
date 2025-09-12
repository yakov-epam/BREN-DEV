from sqlalchemy import Column, String, Enum
from db import enums
from db.models.base import Base, BaseDBModelMixin


class User(Base, BaseDBModelMixin):
    __tablename__ = "users"

    username: str = Column(String(100), nullable=False, unique=True)
    email: str = Column(String(100), nullable=True, default=None, unique=True)
    password: str = Column(String(200), nullable=False)
    role: enums.UserRole = Column(Enum(enums.UserRole), nullable=False)
