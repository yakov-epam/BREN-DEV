from fastapi import APIRouter, Query, Depends, Path, HTTPException
from db.schemas.books import Book, BookCreate, BookUpdate, BookListResponse
from db.repositories.books import BookRepository
from error_handlers.models import ErrorResponse
from v1.resources.books import deps
from math import ceil

ROUTER = APIRouter(prefix="/books", tags=["Books"])


@ROUTER.get("", name="List books", responses={200: {"model": Book}})
async def _(
    id_: int | None = Query(default=None, title="ID filter", gt=0, alias="id"),
    title: str | None = Query(
        default=None, title="Title filter", min_length=1, max_length=100
    ),
    title_like: str | None = Query(
        default=None, title="Title alike filter", max_length=100
    ),
    author: str | None = Query(
        default=None, title="Author filter", min_length=1, max_length=100
    ),
    author_like: str | None = Query(
        default=None, title="Author alike filter", max_length=100
    ),
    pages: int | None = Query(default=None, title="Pages filter", gt=0),
    pages_lt: int | None = Query(default=None, title="Pages less than filter", gt=0),
    pages_gt: int | None = Query(default=None, title="Pages greater than filter", gt=0),
    rating: float | None = Query(default=None, title="Rating filter", ge=0, le=5),
    rating_lt: int | None = Query(
        default=None, title="Rating less than filter", gt=0, le=5
    ),
    rating_gt: int | None = Query(
        default=None, title="Rating greater than filter", gt=0, le=5
    ),
    price: float | None = Query(default=None, title="Price filter", ge=0),
    price_lt: int | None = Query(default=None, title="Price less than filter", gt=0),
    price_gt: int | None = Query(default=None, title="Price greater than filter", gt=0),
    limit: int = Query(default=100, title="Limit of items per page", gt=0),
    page: int = Query(default=1, title="Page", gt=0),
    repo: BookRepository = Depends(deps.get_repo),
):
    filters = {
        "id": id_,
        "title": title,
        "title_like": title_like,
        "author": author,
        "author_like": author_like,
        "pages": pages,
        "pages_lt": pages_lt,
        "pages_gt": pages_gt,
        "rating": rating,
        "rating_lt": rating_lt,
        "rating_gt": rating_gt,
        "price": price,
        "price_lt": price_lt,
        "price_gt": price_gt,
    }
    return BookListResponse(
        items=await repo.get_all(limit=limit, offset=(page - 1) * limit, **filters),
        total_pages=ceil(await repo.count(offset=(page - 1) * limit, **filters) / limit),
    )


@ROUTER.get(
    "/{item_id}",
    name="Get one book",
    responses={
        200: {"model": Book},
        404: {"model": ErrorResponse, "description": "Book not found"},
    },
)
async def _(
    item_id: int = Path(title="Book ID", gt=0),
    repo: BookRepository = Depends(deps.get_repo),
):
    r = await repo.get_one_by_id(item_id)
    if not r:
        raise HTTPException(status_code=404, detail="Book not found")
    return r


@ROUTER.post("", name="Create book", responses={201: {"model": Book}}, status_code=201)
async def _(
    data: BookCreate,
    repo: BookRepository = Depends(deps.get_repo),
):
    return await repo.create_one(data)


@ROUTER.put(
    "/{item_id}",
    name="Update book",
    responses={
        200: {"model": Book},
        404: {"model": ErrorResponse, "description": "Book not found"},
    },
)
async def _(
    data: BookUpdate,
    item_id: int = Path(title="Book ID", gt=0),
    repo: BookRepository = Depends(deps.get_repo),
):
    r = await repo.update_one(item_id, data)
    if not r:
        raise HTTPException(status_code=404, detail="Book not found")
    return r


@ROUTER.delete(
    "/{item_id}",
    name="Delete book",
    responses={
        200: {"model": Book},
        404: {"model": ErrorResponse, "description": "Book not found"},
    },
)
async def _(
    item_id: int = Path(title="Book ID", gt=0),
    repo: BookRepository = Depends(deps.get_repo),
):
    r = await repo.delete_one(item_id)
    if not r:
        raise HTTPException(status_code=404, detail="Book not found")
    return r
