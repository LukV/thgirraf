from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    email: EmailStr
    new_password: str
    token: str

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
    uid: str
    username: str
    email: EmailStr
    icon: Optional[str]
    date_created: datetime

    class Config:
        from_attributes = True
