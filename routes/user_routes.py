from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_db
from utils.swagger_auth import swagger_security
from schemas.user_schema import UserSchema
from controllers.user_controller import (create_user, get_all_users, update_user, delete_user)

router = APIRouter(prefix="/user",tags=["User"],dependencies=[Depends(swagger_security)] )

@router.post("/")
async def add_user(user: UserSchema, db: AsyncSession = Depends(get_async_db)):
    return await create_user(user, db)

@router.get("/")
async def fetch_all_users(db: AsyncSession = Depends(get_async_db)):
    return await get_all_users(db)

@router.put("/{user_id}")
async def edit_user(user_id: int,user: UserSchema,db: AsyncSession = Depends(get_async_db)):
    return await update_user(user_id, user, db)

@router.delete("/{user_id}")
async def remove_user(user_id: int,db: AsyncSession = Depends(get_async_db)):
    return await delete_user(user_id, db)

