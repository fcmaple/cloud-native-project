from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from .security import verify_password, decode_access_token
from .models.user import UserIn
# from .db import fake_users_db

from .db.crud import get_db
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

def authenticate_user( username: str, password: str ,db :Session) -> UserIn:
    # db = get_db()
    userdata = get_user(username, db)
    if userdata is None :
        return False
    if not verify_password(password, userdata.password):
        return False
    return userdata


def get_user( username: str ,db :Session) -> UserIn:
    userdata = db.get_data_users(username)
    print(userdata)
    if isinstance(userdata,str):
        print(userdata)
        return None
    userdata = UserIn(**userdata)
    return userdata
        

def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db:Annotated[Session,Depends(get_db)]) -> UserIn:
    token_data = decode_access_token(token)
    user = get_user(username=token_data.username,db = db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
