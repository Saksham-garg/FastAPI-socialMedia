from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal

class UserCreate(BaseModel):
    email:EmailStr
    password:str


class User(BaseModel):
    id:int
    created_at:datetime

    class Config:   
        orm_mode:True

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str    
    published: bool = False


class PostCreate(PostBase):
    pass


class Post(PostBase):   
    id:int
    created_at:datetime
    owner_id: int   
    owner : UserOut
    class Config:
        orm_mode = True



class LoginUser(UserCreate):
    pass

class LoginToken(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id:int
    dir: Literal[0,1]