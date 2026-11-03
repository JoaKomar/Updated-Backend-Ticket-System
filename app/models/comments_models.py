from sqlalchemy import Boolean, Column, String, DateTime, Integer, ForeignKey
from app.database.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone


class Comments(Base):
    __tablename__ = "comments"

    id = Column(Integer,primary_key=True)
    content = Column(String(200), nullable=False)
    deleted = Column(Boolean, default=False)
    date = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

    user = relationship("Users", back_populates="comments")
    ticket = relationship("Tickets", back_populates="comments")

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tickets_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)