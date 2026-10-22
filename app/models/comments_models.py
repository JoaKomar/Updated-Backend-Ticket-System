from sqlalchemy import Boolean, Column, String, DateTime
from app.database.database import Base
from sqlalchemy.orm import relationship


class Comments(Base):
    __tablename__ = "comments"

    id = Column(primary_key=True,unique=True)
    content = Column(String(200), nullable=False)
    deleted = Column(Boolean, default=False)
    date = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="comments")
    ticket = relationship("Tickets", back_populates="comments")