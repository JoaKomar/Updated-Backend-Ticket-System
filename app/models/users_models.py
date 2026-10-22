from sqlalchemy import Boolean, Column, String, Integer
from app.database.database import Base
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True)
    nombre = Column(String(100), nullable=False)
    edad = Column(Integer, nullable=False)
    email = Column(String(150),nullable=False,unique=True)
    password_hash = Column(String)
    rol = Column(String(20),default="user")
    deleted = Column(Boolean,default=False)

    tickets = relationship("Tickets", back_populates="user")
    comments = relationship("Comments",back_populates="user")