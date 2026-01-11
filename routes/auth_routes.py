from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from controllers.auth_controller import (register_user_controller,set_password_controller,login_controller)
from schemas.auth_schema import (RegisterSchema,SetPasswordSchema, LoginSchema)
from database import get_async_db
from utils.security import get_current_user
from schemas.user_schema import UserSchema

router = APIRouter(prefix="/auth",tags=["Authentication"])

@router.get("/set-password")
async def validate_token(token: str):
    return {"message": "Token is valid.",
        "next_step": "Call POST /auth/set-password with this token and your new password.",
        "token": token}

@router.post("/register")
async def register(data: RegisterSchema, db: AsyncSession = Depends(get_async_db)):
    return await register_user_controller(data, db)

@router.post("/set-password")
async def set_password(data: SetPasswordSchema,db: AsyncSession = Depends(get_async_db)):
    return await set_password_controller(data,db)

@router.post("/login")
async def login(data: LoginSchema,db: AsyncSession = Depends(get_async_db)):
    return await login_controller(data,db)