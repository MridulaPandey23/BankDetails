from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text, Boolean
from database import Base 
class User(Base):
    __tablename__ = "user_details"  

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(Text, nullable=True)
    isverified = Column(Boolean, default=False)
    