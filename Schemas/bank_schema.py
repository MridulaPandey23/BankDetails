from pydantic import BaseModel
from typing import Optional

class BankSchema(BaseModel):
    user_id: int
    acc_num: int
    bank_nm: str

    class Config:
        from_attributes = True 