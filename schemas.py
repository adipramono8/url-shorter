from pydantic import BaseModel, HttpUrl
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