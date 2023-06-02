from typing import Union

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class UserOut(BaseModel):
    username: str
    realname: str
    phone: str
    car: Union[str , None] = None

class UserLogin(UserOut):
    password: str
    
class UserIn(UserLogin):
    user_id: int

