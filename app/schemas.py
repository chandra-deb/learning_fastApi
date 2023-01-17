from datetime import datetime
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
