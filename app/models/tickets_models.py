from sqlalchemy import Boolean, Column, String, Integer, DateTime, ForeignKey
from app.database.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class Tickets(Base):
    __tablename__ = "tickets"

    id = Column(Integer,primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(String(400), nullable=False)
    status = Column(String(150), default="pending")
    deleted = Column(Boolean, default=False)
    date = Column(DateTime, nullable=False, default=datetime.now(timezone.utc).replace(microsecond=0))

    user = relationship("Users", back_populates="tickets")
    comments = relationship("Comments", back_populates="ticket")

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
   