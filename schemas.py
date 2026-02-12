from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class PostBase(BaseModel):
    title: str = Field(..., max_length=100)
    content: str = Field(..., max_length=1000)
    author: str = Field(..., max_length=50)
    
class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    date_posted: datetime
    
    model_config = ConfigDict(from_attributes=True)