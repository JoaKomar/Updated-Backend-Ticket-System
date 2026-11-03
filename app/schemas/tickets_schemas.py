from pydantic import BaseModel, Field
from enum import Enum

class TicketStatus(str,Enum):
    pending = "pending"
    in_process = "in_process"
    completed = "completed"

class TicketUser(BaseModel):
    title: str = Field(min_length=3,max_length=30)
    description: str = Field(min_length=15,max_length=500)
    status: TicketStatus = Field(default=TicketStatus.pending)
  


class TicketAdmin(BaseModel):
    id: int
    title: str = Field(min_length=3,max_length=30)
    description: str = Field(min_length=15,max_length=500)
    status: TicketStatus
    deleted: bool

