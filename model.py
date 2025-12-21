from sqlalchemy import Column, ForeignKey, Integer, String
from database import Base

class BankDetails(Base):
    __tablename__ = "bank_details"
    user_id = Column(Integer, ForeignKey("user_details.id"), primary_key=True)
    acc_num = Column(Integer, unique=True, index=True)
    bank_nm = Column(String, index=True)


