from sqlalchemy import Column, Integer, String
from database import Base

class BankDetails(Base):
    __tablename__ = "bank_details"

    acc_num = Column(Integer, primary_key=True)
    bank_nm = Column(String, unique=True, index=True)


