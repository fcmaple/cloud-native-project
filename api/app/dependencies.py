from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from .security import verify_password, decode_access_token
from .models.user import UserIn
from .db import fake_users_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


def authenticate_user(fake_db, username: str, password: str) -> UserIn:
    userdata = get_user(fake_db, username)
    if not userdata:
        return False
    if not verify_password(password, userdata.password):
        return False
    return userdata


def get_user(db, username: str) -> UserIn:
    if username in db:
        userdata = db[username]
        return UserIn(**userdata)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserIn:
    token_data = decode_access_token(token)
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
