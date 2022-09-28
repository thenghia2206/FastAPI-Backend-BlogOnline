from datetime import datetime
from typing import Optional
from pydantic import BaseModel,EmailStr

class PostBase(BaseModel):
    title: str
    content: str
    thumnai= str
    desciption : str
    category_id: int

class Category(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode= True

class LikedPost(BaseModel):
    id: int
    class Config:
        orm_mode= True
    

class LikedPostCreate(LikedPost):
    user_id: int
    post_id: int

class PostCreate(PostBase):
    pass

class CommentBase(BaseModel):
    content: str

    
class CommentCreate(CommentBase):
    pass 

class Comment(CommentBase):
    id: int
    user_id: int
    post_id: int
    createdOn: datetime
    updateOn: datetime
    name: str
    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: int
    post_status: int
    cmt_status: int
    username: str
    name: str
    class Config:
        orm_mode = True

class BanDays(BaseModel):
    days: int

class Post(PostBase):
    id: int
    createdOn: datetime
    updateOn: datetime
    owner_id: int
    owner : UserOut
    category: Category
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None   