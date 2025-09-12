from pydantic import BaseModel, Field, ConfigDict


class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=100, title="Title")
    author: str = Field(min_length=1, max_length=100, title="Author")
    pages: int = Field(gt=0, title="Pages")
    rating: float = Field(gt=0, le=5, title="Rating")
    price: float = Field(ge=0, title="Price")


class Book(BookBase):
    id: int | None = Field(default=None, title="ID", gt=0)

    model_config = ConfigDict(from_attributes=True)


class BookCreate(BookBase):
    id: int | None = Field(default=None, title="ID", gt=0)


class BookUpdate(BookBase):
    title: str | None = Field(default=None, min_length=1, max_length=100, title="Title")
    author: str | None = Field(default=None, min_length=1, max_length=100, title="Author")
    pages: int | None = Field(default=None, gt=0, title="Pages")
    rating: float | None = Field(default=None, gt=0, le=5, title="Rating")
    price: float | None = Field(default=None, ge=0, title="Price")


class BookListResponse(BaseModel):
    items: list[Book] = Field(title="Book list", description="A list of book objects")
    total_pages: int = Field(title="Total pages")
