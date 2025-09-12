from typing import Any
from sqlalchemy import select, Select, func
from sqlalchemy.orm import Query

from .abstract import AbstractRepository
from db.models import books as models
from db.schemas import books as schemas


class BookRepository(AbstractRepository):
    @staticmethod
    def _prepare_filtered_query(
        stmt: Select[Any] | Query | None, filters: dict
    ) -> Select | Query[Any]:
        """
        Apply filter to a query.
        :param stmt: Query to filter.
        :param filters: Filters to apply.
        :return: Filtered query.
        """
        for k, v in filters.items():
            if v is None:
                continue
            k, _, action = k.partition("_")
            if action:
                if action == "lt":
                    stmt = stmt.filter(getattr(models.Book, k) < v)  # noqa
                elif action == "gt":
                    stmt = stmt.filter(getattr(models.Book, k) > v)  # noqa
                elif action == "like":
                    stmt = stmt.filter(getattr(models.Book, k).ilike(f"%{v}%"))
            else:
                stmt = stmt.filter(getattr(models.Book, k) == v)  # noqa
        return stmt

    async def get_all(
        self, limit: int = 100, offset: int = 0, **filters
    ) -> list[schemas.Book]:
        """
        Get all books.
        :param limit: Limit of books to look for.
        :param offset: Offset of books to look for.
        :param filters: Optional filters.
        :return: A sequence of books.
        """
        stmt = self._prepare_filtered_query(
            select(models.Book).limit(limit).offset(offset), filters
        )
        return [
            schemas.Book.model_validate(i)
            for i in self.session.execute(stmt).scalars().all()
        ]

    async def count(self, offset: int = 0, **filters) -> int:
        """
        Count the number of matching books.
        :param offset: Offset of books to look for.
        :param filters: Optional filters.
        :return: Total books found.
        """
        return self._prepare_filtered_query(
            self.session.query(func.count(models.Book.id)), filters
        ).scalar()

    async def get_one_by_property(self, name: str, value: Any) -> schemas.Book | None:
        """
        Get one book by property.
        :param name: Property name.
        :param value: Property value.
        :return: Found book or None.
        """
        stmt = self._prepare_filtered_query(select(models.Book), {name: value})
        r = self.session.execute(stmt).scalars().first()
        return r

    async def create_one(self, data: schemas.BookCreate) -> schemas.Book:
        """
        Create one book.
        :param data: Book to create.
        :return: Created book.
        """
        item = models.Book(**data.model_dump())
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    async def update_one(
        self, id_: int, new_data: schemas.BookUpdate
    ) -> schemas.Book | None:
        """
        Update one book.
        :param id_: Book ID.
        :param new_data: Book with new data to propagate to the database.
        :return: Updated book.
        """
        item = await self.get_one_by_id(id_)
        if not item:
            return None
        for k, v in new_data.model_dump(exclude_unset=True).items():
            setattr(item, k, v)
        self.session.commit()
        self.session.refresh(item)
        return item

    async def delete_one(self, id_: int) -> schemas.Book | None:
        """
        Delete one book.
        :param id_: Book ID.
        :return: Deleted book.
        """
        item = await self.get_one_by_id(id_)
        if not item:
            return None
        self.session.delete(item)
        self.session.commit()
        return item
