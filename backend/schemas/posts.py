from datetime import datetime
from pydantic import BaseModel

class PostCreate(BaseModel):
    text: str

class PostResponse(BaseModel):
    id: int
    pid: str
    text: str
    date_created: datetime

    class Config:
        from_attributes = True
