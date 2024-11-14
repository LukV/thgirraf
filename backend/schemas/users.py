from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: Optional[str] = None
    icon: Optional[str] = None

class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    icon: Optional[str]

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    icon: Optional[str]
    date_created: datetime

    class Config:
        orm_mode = True
