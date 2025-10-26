from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from dbSetup import Base 

class Link(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True, index=True)
    long_url = Column(String, index=True, nullable=False)
    short_url = Column(String, unique=True, index=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())