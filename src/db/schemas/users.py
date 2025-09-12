from pydantic import BaseModel, Field, EmailStr, ConfigDict
from db import enums
from db.schemas.base import BaseListResponse


class UserBase(BaseModel):
    username: str = Field(
        title="Username", min_length=1, max_length=100, pattern=r"^[a-zA-Z0-9_]+$"
    )
    email: EmailStr | None = Field(
        default=None, title="Email", min_length=1, max_length=100
    )


class UserCreate(UserBase):
    role: enums.UserRole | None = Field(default=None, title="User role")
    password: str = Field(title="Password", min_length=8, max_length=100)


class UserUpdate(UserCreate):
    username: str | None = Field(
        default=None,
        title="Username",
        min_length=1,
        max_length=100,
        pattern=r"^[a-zA-Z0-9_]+$",
    )
    email: EmailStr | None = Field(
        default=None, title="Email", min_length=1, max_length=100
    )
    password: str | None = Field(
        default=None, title="Password", min_length=8, max_length=100
    )


class User(UserBase):
    id: int = Field(title="ID", gt=0)
    role: enums.UserRole = Field(title="User role")

    model_config = ConfigDict(from_attributes=True, extra="ignore")


class UserListResponse(BaseListResponse):
    items: list[User] = Field(title="User list", description="A list of user objects")


class UserTokenResponse(BaseModel):
    access_token: str = Field(title="Access token")
    token_type: str = Field(title="Token type")
    user: User = Field(title="User")
