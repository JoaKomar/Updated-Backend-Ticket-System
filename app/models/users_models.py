from sqlalchemy import Boolean, Column, String, Integer, ForeignKey
from app.database.database import Base
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String(150),nullable=False,unique=True)
    password_hash = Column(String(100))
    role = Column(String(20),default="user")
    deleted = Column(Boolean,default=False)

    tickets = relationship("Tickets", back_populates="user")
    comments = relationship("Comments",back_populates="user")
