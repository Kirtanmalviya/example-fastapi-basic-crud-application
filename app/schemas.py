
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from pydantic.types import conint

class PostBase(BaseModel): # schema Validation
    title: str
    content: str
    published: bool = True # default value is True, if we don't provide a value for published, it will be set to True.

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr 
    created_at: datetime

    class Config:
        from_attributes = True

class Post(BaseModel):
    title: str
    content: str
    published: bool
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True # this will tell Pydantic to read the data even if it is not a dict, 
        #but an ORM model (like SQLAlchemy model)

class voteModel(BaseModel):
    Post: Post
    votes: int

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int

class VoteModel(BaseModel):
    post_id: int
    dir: conint(le=1)