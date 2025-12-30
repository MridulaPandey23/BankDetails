from pydantic import BaseModel
from typing import Optional
from schemas.userBankSchema import BankSchema
class UserSchema(BaseModel):
    name : str
    age : int
    gender : str
    email : str
    bank: Optional[BankSchema] = None 

    class Config:
        from_attributes = True 