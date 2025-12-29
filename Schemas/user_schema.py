from pydantic import BaseModel
from schemas.bank_schema import BankSchema

class UserSchema(BaseModel):
    name : str
    age : int
    gender : str
    email : str
    bank : BankSchema

    class Config:
        from_attributes = True 