from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=True)  # Optional for Google login users
    icon = Column(String, nullable=True)
    date_created = Column(DateTime(timezone=True), server_default=func.now()) # pylint: disable=E1102
    google_login = Column(Boolean, default=False)  # Distinguish Google login users

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    pid = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    text = Column(String, nullable=False)
    date_created = Column(DateTime(timezone=True), server_default=func.now()) # pylint: disable=E1102
