from pydantic import BaseModel
from pydantic import EmailStr

class RegisterSchema(BaseModel):
    name: str
    email: EmailStr

class SetPasswordSchema(BaseModel):
    token: str
    password: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str
