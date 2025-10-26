from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from dbSetup import Base 

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    google_id = Column(String, unique=True, index=True, nullable=True)
    # --------------------------------------------------------------------- #
    links = relationship("Link", back_populates="owner")

class Link(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True, index=True)
    long_url = Column(String, index=True, nullable=False)
    short_url = Column(String, unique=True, index=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))
    # --------------------------------------------------------------------- #
    owner = relationship("User", back_populates="links")