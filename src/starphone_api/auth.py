from datetime import UTC, datetime, timedelta
from functools import partial
from typing import Callable

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from pydantic import BaseModel
from sqlmodel import Session, select

from starphone_api.config import settings
from starphone_api.models import User
from starphone_api.security import verify_password
from starphone_api.db import engine

SECRET_KEY = settings.security.secret_key  # pyright: ignore[reportOptionalMemberAccess, reportAttributeAccessIssue]
ALGORITHM = settings.security.algorithm  # pyright: ignore[reportOptionalMemberAccess, reportAttributeAccessIssue]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshToken(BaseModel):
    refresh_token: str


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
    scope: str = "access_token",
) -> str:
    """Create a JWT Token from user data.

    scope: access_token or refresh_token
    """
    to_encode = data.copy()

    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire, "scope": scope})

    return jwt.encode(
        to_encode,
        SECRET_KEY,  # pyright: ignore[reportArgumentType]
        algorithm=ALGORITHM,  # pyright: ignore[reportArgumentType]
    )


create_refresh_token = partial(create_access_token, scope="refresh_token")


def authenticate_user(
    get_user: Callable,
    username: str,
    password: str,
) -> User | bool:
    """Verify if user exists and password is correct."""

    user = get_user(username)

    if not user:
        return False

    if not verify_password(plain_password=password, hashed_password=user.password):
        return False

    return user


def get_user(username: str | None) -> User | None:
    query = select(User).where(User.username == username)
    with Session(engine) as session:
        return session.exec(query).first()


def get_current_user(
    token: str = Depends(oauth2_scheme),
):
    """Return the authenticated user based on the JWT bearer token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token:
        raise credentials_exception

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,  # pyright: ignore[reportArgumentType]
            algorithms=[ALGORITHM],  # pyright: ignore[reportArgumentType]
        )

    except PyJWTError:
        raise credentials_exception

    username: str | None = payload.get("sub")
    if not username:
        raise credentials_exception

    user = get_user(username=username)
    if user is None:
        raise credentials_exception

    return user


async def validate_token(token: str = Depends(oauth2_scheme)) -> User:
    user = get_current_user(token=token)
    return user
