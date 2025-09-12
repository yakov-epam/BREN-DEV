from abc import ABC, abstractmethod
from typing import TypeVar, Any
from sqlalchemy.orm import Session

T = TypeVar("T")
SchemaT = TypeVar("SchemaT")
UpdateT = TypeVar("UpdateT")
CreateT = TypeVar("CreateT")


class AbstractRepository(ABC):
    def __init__(self, session: Session) -> None:
        self.session = session

    @abstractmethod
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

    @abstractmethod
    async def count(self, offset: int = 0, **filters) -> int:
        """
        Count the number of matching items.
        :param offset: Offset of items to look for.
        :param filters: Optional filters.
        :return: Total records found.
        """

    @abstractmethod
    async def get_one_by_property(self, name: str, value: Any) -> SchemaT | None:
        """
        Get one item by property.
        :param name: Property name.
        :param value: Property value.
        :return: Found item or None.
        """

    async def get_one_by_id(self, id_: int) -> SchemaT | None:
        """
        Get one item.
        A shortcut for `get_one_by_property`.
        Can also be used to check if item exists.
        :param id_: Item ID.
        :return: Found item or None.
        """
        return await self.get_one_by_property("id", id_)

    @abstractmethod
    async def create_one(self, data: CreateT) -> SchemaT:
        """
        Create one item.
        :param data: Item to create.
        :return: Created item.
        """

    @abstractmethod
    async def update_one(self, id_: int, new_data: UpdateT) -> SchemaT | None:
        """
        Update one item.
        :param id_: Item ID.
        :param new_data: Item with new data to propagate to the database.
        :return: Updated item.
        """

    @abstractmethod
    async def delete_one(self, id_: int) -> SchemaT | None:
        """
        Delete one item.
        :param id_: Item ID.
        :return: Deleted item.
        """
