from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str    
    published: bool = False


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id:int
    created_at:datetime

    class Config:
        orm_mode = True




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

class LoginUser(UserCreate):
    pass