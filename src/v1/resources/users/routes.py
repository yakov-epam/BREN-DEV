from fastapi import APIRouter, Query, Depends, Path, HTTPException

from db.repositories.users import UserRepository, get_repo
from db.schemas.users import User, UserCreate, UserUpdate, UserListResponse
from error_handlers.models import ErrorResponse
from db import enums
from math import ceil
from v1.security import get_user, get_admin

ROUTER = APIRouter(prefix="/users", tags=["Users"])


@ROUTER.get(
    "",
    name="List users",
    responses={200: {"model": User, "description": "OK"}},
    dependencies=[Depends(get_user)],
)
async def _(
    id_: int | None = Query(default=None, title="ID filter", gt=0, alias="id"),
    username: str | None = Query(
        default=None, title="Username filter", min_length=1, max_length=100
    ),
    username_like: str | None = Query(
        default=None, title="Username alike filter", max_length=100
    ),
    email: str | None = Query(
        default=None, title="Email filter", min_length=1, max_length=100
    ),
    email_like: str | None = Query(
        default=None, title="Email alike filter", max_length=100
    ),
    role: enums.UserRole | None = Query(default=None, title="Role filter", gt=0),
    limit: int = Query(default=100, title="Limit of items per page", gt=0),
    page: int = Query(default=1, title="Page", gt=0),
    repo: UserRepository = Depends(get_repo),
):
    filters = {
        "id": id_,
        "username": username,
        "username_like": username_like,
        "email": email,
        "email_like": email_like,
        "role": role,
    }
    return UserListResponse(
        items=await repo.get_all(limit=limit, offset=(page - 1) * limit, **filters),
        total_pages=ceil(await repo.count(offset=(page - 1) * limit, **filters) / limit),
    )


@ROUTER.get(
    "/{item_id}",
    name="Get one user",
    responses={
        200: {"model": User, "description": "OK"},
        404: {"model": ErrorResponse, "description": "User not found"},
    },
    dependencies=[Depends(get_user)],
)
async def _(
    item_id: int = Path(title="User ID", gt=0),
    repo: UserRepository = Depends(get_repo),
):
    r = await repo.get_one_by_id(item_id)
    if not r:
        raise HTTPException(status_code=404, detail="User not found")
    return r


@ROUTER.post(
    "",
    name="Create user",
    responses={
        201: {"model": User, "description": "OK"},
        409: {"model": ErrorResponse, "description": "Username or email already taken"},
    },
    status_code=201,
    dependencies=[Depends(get_admin)],
)
async def _(
    data: UserCreate,
    repo: UserRepository = Depends(get_repo),
):
    if data.role is None:
        data.role = enums.UserRole.USER
    r = await repo.create_one(data)
    if not r:
        raise HTTPException(status_code=409, detail="Conflict")
    return r


@ROUTER.put(
    "/{item_id}",
    name="Update user",
    responses={
        200: {"model": User, "description": "OK"},
        403: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "User not found or conflict"},
    },
)
async def _(
    data: UserUpdate,
    item_id: int = Path(title="User ID", gt=0),
    repo: UserRepository = Depends(get_repo),
    user: User = Depends(get_user),
):
    if user.id != item_id and user.role != enums.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Unauthorized")
    r = await repo.update_one(item_id, data)
    if not r:
        raise HTTPException(status_code=404, detail="User not found or conflict")
    return r


@ROUTER.delete(
    "/{item_id}",
    name="Delete user",
    responses={
        200: {"model": User, "description": "OK"},
        404: {"model": ErrorResponse, "description": "User not found"},
    },
)
async def _(
    item_id: int = Path(title="User ID", gt=0),
    repo: UserRepository = Depends(get_repo),
    user: User = Depends(get_user),
):
    if user.id != item_id and user.role != enums.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Unauthorized")
    r = await repo.delete_one(item_id)
    if not r:
        raise HTTPException(status_code=404, detail="User not found")
    return r
