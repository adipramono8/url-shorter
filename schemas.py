from pydantic import BaseModel, HttpUrl
from pydantic import ConfigDict
import datetime

# Data Schema for creating a new URL entry
class newURL(BaseModel):
    long_url: HttpUrl

# Data Schema for returning URL information
class responseURL(BaseModel):
    long_url: HttpUrl
    short_url: str
    created_at: datetime.datetime
    # Make Pydantnic to read ORM models
    class Config:
        orm_mode = True

# Below here are user related schemas
class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None