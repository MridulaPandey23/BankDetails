from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_db

from schemas.bankSchema import BankSchema
from schemas.userSchema import UserSchema

from controllers.bankController import (create_bank_details,get_bank_details,get_bank,update_bank_details,delete_bank_details,get_user_bank_details)

router = APIRouter(prefix="/bank", tags=["Bank"])

# ---------------- BANK ROUTES ----------------

@router.post("/bank/")
async def create_bank(bank: BankSchema, db: AsyncSession = Depends(get_async_db)):
    return await create_bank_details(bank, db)


@router.get("/bank/")
async def get_all_banks(db: AsyncSession = Depends(get_async_db)):
    return await get_bank_details(db)

@router.get("/user/{user_id}")
async def fetch_user(bank_id: int, db: AsyncSession = Depends(get_async_db)):
    return await get_bank(bank_id, db)

@router.put("/bank/{id}")
async def update_bank(id: int, bank: BankSchema, db: AsyncSession = Depends(get_async_db)):
    return await update_bank_details(id, bank, db)

@router.delete("/bank/{id}")
async def delete_bank(id: int, db: AsyncSession = Depends(get_async_db)):
    return await delete_bank_details(id, db)


# -------- USER + BANK COMBINED --------

@router.get("/userbank/{user_id}")
async def fetch_user_bank(user_id: int, db: AsyncSession = Depends(get_async_db)):
    return await get_user_bank_details(user_id, db)
