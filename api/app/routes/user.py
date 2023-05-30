from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm

from ..models.user import UserOut, UserIn, Token
# from ..db import fake_users_db
from ..dependencies import get_current_user, authenticate_user
from ..security import create_access_token, hashing_password
from ..config import settings

from sqlalchemy.orm import Session
# from ..db.database import get_db_session
# from ..db.crud import process_data
from ..db.crud import get_db

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "API or Database Server Error"}
    }
)

# def get_db():
#     _db = next(get_db_session())
#     try:
#         yield process_data(_db)
#     finally:
#         _db.close()


@router.get(
    "",
    response_model=UserOut,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Could not validate credentials"}
    }
)
def read_user_info(
    userdata: Annotated[UserIn, Depends(get_current_user)],
):
    return userdata


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"content": None},
        status.HTTP_409_CONFLICT: {"description": "User already exists"}
    }
)
def register_user(
    userdata: UserIn,
    db: Annotated[Session,Depends(get_db)],
):
    # if userdata.username in fake_users_db:
    #     raise HTTPException(
    #             status_code=status.HTTP_409_CONFLICT,
    #             detail="User already exists")

    userdata.password = hashing_password(userdata.password)
    user = userdata.dict()
    del user["user_id"]
    a = db.insert_data_users(user)

    return Response(status_code=status.HTTP_201_CREATED)


@router.post(
    "/login",
    response_model=Token,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Incorrect username or password"}
    }
)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session,Depends(get_db)],
):
    user = authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}
