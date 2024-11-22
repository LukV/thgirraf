from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class PostCreate(BaseModel):
    text: str

class PostResponse(BaseModel):
    id: int
    pid: str
    user_id: int
    text: str
    title: Optional[str]
    description: Optional[str]
    image_url: Optional[str]
    date_created: datetime

    class Config:
        from_attributes = True
