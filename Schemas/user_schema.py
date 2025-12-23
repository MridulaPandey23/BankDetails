from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    name : Optional[str] = None
    age : Optional[int] = None
    gender : Optional[str] = None
    email : Optional[str] = None

    class Config:
        from_attributes = True 