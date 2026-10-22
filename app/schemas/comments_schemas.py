from pydantic import BaseModel, Field

class CommentsUser(BaseModel):
    content: str = Field(min_length=15,max_length=500)

class CommentAdmin(BaseModel):
    id : int
    content : str = Field(min_length=15,max_length=500)
    deleted : str 
    date : str

