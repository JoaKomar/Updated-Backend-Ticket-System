from sqlalchemy import Boolean, Column, String, Integer, DateTime
from app.database.database import Base
from sqlalchemy.orm import relationship


class Tickets(Base):
    __tablename__ = "tickets"

    id = Column(Integer,primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(String(400), nullable=False)
    status = Column(String(150), default="close")
    deleted = Column(Boolean, default=False)
    date = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="tickets")
    comments = relationship("Comments", back_populates="ticket")