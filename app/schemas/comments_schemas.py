from pydantic import BaseModel, Field
from datetime import datetime

class CommentsUser(BaseModel):
    content: str = Field(min_length=15,max_length=200)

class CommentAdmin(BaseModel):
    id : int
    content : str = Field(min_length=15,max_length=200)
    deleted : bool 
    date : datetime

