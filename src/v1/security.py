from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timezone, timedelta
from const import SETTINGS
from db.repositories.users import UserRepository, get_repo
from db.schemas.users import User
from db import enums
import jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/auth")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=SETTINGS.app.jwt_exp_minutes)
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(
        to_encode, SETTINGS.app.jwt_secret, algorithm=SETTINGS.app.jwt_algo
    )
    return encoded_jwt


async def check_user_auth(
    token: str = Depends(oauth2_scheme), repo: UserRepository = Depends(get_repo)
) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, SETTINGS.app.jwt_secret, algorithms=[SETTINGS.app.jwt_algo]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = await repo.get_one_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user


async def get_user(user: User = Depends(check_user_auth)):
    if user.role not in (enums.UserRole.USER, enums.UserRole.ADMIN):
        raise HTTPException(status_code=403, detail="Unauthorized")
    return user


async def get_admin(user: User = Depends(check_user_auth)):
    if user.role != enums.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return user
