from sqlalchemy import Column, String, Integer, Float
from .base import Base


class Book(Base):
    __tablename__ = "books"

    id: int = Column(Integer, primary_key=True, nullable=False)
    title: str = Column(String(100), nullable=False)
    author: str = Column(String(100), nullable=False)
    pages: int = Column(Integer, nullable=False)
    rating: float = Column(Float, nullable=False)
    price: float = Column(Float, nullable=False)
