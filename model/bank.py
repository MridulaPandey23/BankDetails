from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String
from database import Base

class BankDetails(Base):
    __tablename__ = "bank_details"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_details.id", ondelete="CASCADE"))
    acc_num = Column(BigInteger, nullable=True)
    bank_nm = Column(String(100), nullable=True)