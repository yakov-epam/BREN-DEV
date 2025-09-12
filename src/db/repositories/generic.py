from typing import Any, TypeVar, Generic, Type
from sqlalchemy import select, Select, func
from sqlalchemy.orm import Query, Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel

from .abstract import AbstractRepository
from db.models.base import BaseDBModelMixin

ModelT = TypeVar("ModelT", bound=BaseDBModelMixin)
SchemaT = TypeVar("SchemaT", bound=BaseModel)
CreateSchemaT = TypeVar("CreateSchemaT", bound=BaseModel)
UpdateSchemaT = TypeVar("UpdateSchemaT", bound=BaseModel)


class GenericRepository(
    AbstractRepository, Generic[ModelT, SchemaT, CreateSchemaT, UpdateSchemaT]
):
    def __init__(self, session: Session, model: Type[ModelT], schema: Type[SchemaT]):
        super().__init__(session)
        self.model = model
        self.schema = schema

    def _prepare_filtered_query(
        self, stmt: Select[Any] | Query | None, filters: dict
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
                    stmt = stmt.filter(getattr(self.model, k) < v)
                elif action == "gt":
                    stmt = stmt.filter(getattr(self.model, k) > v)
                elif action == "like":
                    stmt = stmt.filter(getattr(self.model, k).ilike(f"%{v}%"))
            else:
                stmt = stmt.filter(getattr(self.model, k) == v)  # noqa
        return stmt

    async def get_all(
        self, limit: int = 100, offset: int = 0, **filters
    ) -> list[SchemaT]:
        """
        Get all items.
        :param limit: Limit of items to look for.
        :param offset: Offset of items to look for.
        :param filters: Optional filters.
        :return: A sequence of items.
        """
        stmt = self._prepare_filtered_query(
            select(self.model).limit(limit).offset(offset), filters
        )
        return [
            self.schema.model_validate(i)
            for i in self.session.execute(stmt).scalars().all()
        ]

    async def count(self, offset: int = 0, **filters) -> int:
        """
        Count the number of matching items.
        :param offset: Offset of items to look for.
        :param filters: Optional filters.
        :return: Total items found.
        """
        return self._prepare_filtered_query(
            self.session.query(func.count(self.model.id)), filters
        ).scalar()

    async def get_one_by_property(
        self, name: str, value: Any, raw: bool = False
    ) -> SchemaT | ModelT | None:
        """
        Get one item by property.
        :param name: Property name.
        :param value: Property value.
        :param raw: Return raw value.
        :return: Found item or None.
        """
        stmt = self._prepare_filtered_query(select(self.model), {name: value})
        r = self.session.execute(stmt).scalars().first()
        if not r:
            return None
        return self.schema.model_validate(r) if not raw else r

    async def create_one(self, data: CreateSchemaT) -> SchemaT | None:
        """
        Create one item.
        :param data: Item to create.
        :return: Created item.
        """
        try:
            item = self.model(**data.model_dump())
            self.session.add(item)
            self.session.commit()
            self.session.refresh(item)
        except IntegrityError:
            return None
        return self.schema.model_validate(item)

    async def update_one(self, id_: int, new_data: UpdateSchemaT) -> SchemaT | None:
        """
        Update one item.
        :param id_: Item ID.
        :param new_data: Item with new data to propagate to the database.
        :return: Updated item.
        """
        try:
            item = await self.get_one_by_id(id_, raw=True)
            if not item:
                return None
            for k, v in new_data.model_dump(exclude_unset=True).items():
                setattr(item, k, v)
            self.session.commit()
            self.session.refresh(item)
        except IntegrityError:
            return None
        return self.schema.model_validate(item)

    async def delete_one(self, id_: int) -> SchemaT | None:
        """
        Delete one item.
        :param id_: Item ID.
        :return: Deleted item.
        """
        item = await self.get_one_by_id(id_, raw=True)
        if not item:
            return None
        self.session.delete(item)
        self.session.commit()
        return self.schema.model_validate(item)
