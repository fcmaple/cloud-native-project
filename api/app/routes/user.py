from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm

from ..models.user import UserOut, UserIn, UserLogin, Token
from ..dependencies import get_current_user, authenticate_user
from ..security import create_access_token, hashing_password
from ..config import settings

from sqlalchemy.orm import Session
from ..db.crud import get_db

import logging
router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "API or Database Server Error"}
    }
)

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
    logging.info(f"API function: read_user_info , return {userdata}")
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
    userdata: UserLogin,
    db: Annotated[Session,Depends(get_db)],
):
    # if userdata.username in fake_users_db:
    #     raise HTTPException(
    #             status_code=status.HTTP_409_CONFLICT,
    #             detail="User already exists")

    userdata.password = hashing_password(userdata.password)
    user = userdata.dict()
    db.insert_data_users(user)
    logging.info(f"API function: register_user ,userdata :{userdata}")
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
        logging.warning("API function: login_for_access_token ,error: Incorrect username or password")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    res = {"access_token": access_token, "token_type": "bearer"}
    logging.info(f"API function: login_for_access_token ,Return {res}")
    return res
