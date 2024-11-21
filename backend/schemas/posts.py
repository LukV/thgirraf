from datetime import datetime
from pydantic import BaseModel

class PostCreate(BaseModel):
    text: str

class PostResponse(BaseModel):
    id: int
    pid: str
    user_id: int
    text: str
    date_created: datetime

    class Config:
        from_attributes = True
