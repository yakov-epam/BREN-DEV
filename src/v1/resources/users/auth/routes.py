from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext

from db.repositories.users import UserRepository, get_repo
from db.schemas.users import UserTokenResponse
from fastapi.security import OAuth2PasswordRequestForm
from error_handlers.models import ErrorResponse
from v1.security import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ROUTER = APIRouter(prefix="/auth", tags=["Users"])


@ROUTER.post(
    "",
    name="Login",
    responses={
        200: {"model": UserTokenResponse, "description": "Login successful"},
        401: {"model": ErrorResponse, "description": "Invalid credentials"},
    },
)
async def _(
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
    repo: UserRepository = Depends(get_repo),
):
    exc = HTTPException(status_code=401, detail="Invalid credentials")
    user = await repo.get_one_by_property("email", form_data.username, raw=True)
    if not user:
        user = await repo.get_one_by_property("username", form_data.username, raw=True)
    if not user:
        raise exc

    if not pwd_context.verify(form_data.password, user.password):
        raise exc

    return UserTokenResponse(
        access_token=create_access_token({"sub": str(user.id)}),
        token_type="bearer",
        user=user,
    )
