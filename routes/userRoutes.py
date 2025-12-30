from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_db
from schemas.userSchema import UserSchema
from controllers.userController import (create_user,get_user,get_all_users,update_user,delete_user)

router = APIRouter(prefix="/user", tags=["User"])


# ---------------- USER ROUTES ----------------

@router.post("/")
async def add_user(user: UserSchema, db: AsyncSession = Depends(get_async_db)):
    return await create_user(user, db)
    

@router.get("/user/{user_id}")
async def fetch_user(user_id: int, db: AsyncSession = Depends(get_async_db)):
    return await  get_user(user_id, db)


@router.get("/")
async def fetch_all_users(db: AsyncSession = Depends(get_async_db)):
    return await get_all_users(db)


@router.put("/user/{user_id}")
async def edit_user(user_id: int, user: UserSchema, db: AsyncSession = Depends(get_async_db)):
    return await update_user(user_id, user, db)


@router.delete("/user/{user_id}")
async def remove_user(user_id: int, db: AsyncSession = Depends(get_async_db)):
    return await delete_user(user_id, db)

