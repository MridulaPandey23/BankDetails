from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, ForeignKey , Text, Boolean, DateTime
from database import Base 

class PasswordToken(Base):
    __tablename__ = "password_tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user_details.id"))
    token = Column(Text, unique=True)
    expires_at = Column(DateTime)
    is_used = Column(Boolean, default=False)
