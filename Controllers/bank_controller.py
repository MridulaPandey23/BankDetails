from fastapi import HTTPException, Depends
from model.bank import BankDetails
from model.user import User
from schemas.bank_schema import BankSchema
from database import get_async_db
from utils.response_wrapper import api_response
from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession

# BANK DETAILS

# Create Bank Details

async def create_bank_details(bank: BankSchema, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(User).where(User.id == bank.user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        query = text("INSERT INTO bank_details (user_id, acc_num, bank_nm) VALUES (:user_id, :acc_num, :bank_nm) RETURNING id, user_id, acc_num, bank_nm")
        result = await db.execute(query, {"user_id": bank.user_id, "acc_num": bank.acc_num, "bank_nm": bank.bank_nm})
        await db.commit()
        row = result.mappings().one()
        return api_response(
            data=[{"id": row["id"],"user_id": row["user_id"],"acc_num": row["acc_num"],"bank_nm": row["bank_nm"]}],message="Bank account added successfully")
    except Exception as e:
        print("GENERAL ERROR:", e)
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create bank details")


# Get all Bank Details

async def get_bank_details(db: AsyncSession = Depends(get_async_db)):
    try:
        query = text("SELECT * FROM bank_details")
        result = await db.execute(query)
        rows = result.mappings().all()
        data = [{"user_id": row["user_id"],"id": row["id"], "bank_nm": row["bank_nm"], "acc_num": row["acc_num"] }for row in rows]
        return api_response(data=data, message="Users retrieved successfully")
    except Exception as e:
        print("GENERAL ERROR:", e)
        raise HTTPException(status_code=500, detail="Failed to retrieve users")

# Get bank by id

async def get_bank(bank_id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        query = text("Select id, acc_num, bank_nm, user_id from bank_details where id = :id ")
        result = await db.execute(query, {"id": bank_id})
        row = result.mappings().first()
        if not row:
            raise HTTPException(status_code=404, detail="Bank not found")
        data = [{ "id": row["id"], "acc_num": row["acc_num"], "bank_nm": row["bank_nm"], "user_id": row["user_id"]}]
        return api_response(data=data, message="Bank details retrieved successfully")
    except Exception as e:
        print("GENERAL ERROR:", e)

# Update Bank Details by User ID

async def update_bank_details(bank_id: int, bank: BankSchema, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(BankDetails).where(BankDetails.id == bank_id))
    existing = result.scalar_one_or_none()                          
    if not existing:
        raise HTTPException(status_code=404, detail="Bank details not found")
    try:
        query = text("UPDATE bank_details SET acc_num = :acc_num, bank_nm = :bank_nm WHERE id = :id RETURNING id, user_id, acc_num, bank_nm")
        result = await db.execute(query, {"id": bank_id, "acc_num": bank.acc_num, "bank_nm": bank.bank_nm})
        await db.commit()
        row = result.mappings().one()
        return api_response(data=[{"id": row["id"], "user_id": row["user_id"], "acc_num": row["acc_num"], "bank_nm": row["bank_nm"]}],message="Bank details updated successfully")
    except Exception as e:
        print("GENERAL ERROR:", e)
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update bank details")



# Delete Bank Details by User ID

async def delete_bank_details(bank_id: int, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute (select(BankDetails).where(BankDetails.id == bank_id))
    existing = result.scalar_one_or_none()
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        query = text("DELETE from bank_details Where id = :id")
        await db.execute(query, {"id": bank_id})
        await db.commit()
        return api_response(message="Bank details deleted successfully")
    except Exception as e:
        print("GENERAL ERROR:", e)
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete bank details")  

# Get User along with Bank Details by User ID

async def get_user_bank_details(user_id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        query = text("SELECT u.id, u.name, u.age, u.gender ,u.email, b.user_id, b.acc_num, b.bank_nm FROM user_details u LEFT JOIN bank_details b ON u.id = b.user_id WHERE u.id = :user_id")
        result = await db.execute(query, {"user_id": user_id})
        row = result.mappings().first()
        if not row:
            raise HTTPException(status_code=404, detail="User not found")
        data = [{"id": row["id"],"name": row["name"],"age": row["age"],"gender": row["gender"],"email": row["email"],"user_id": row["user_id"],"acc_num": row["acc_num"],"bank_nm": row["bank_nm"]}]
        return api_response(data=data,message="User and bank details retrieved successfully")       
    except Exception as e:
        print("GENERAL ERROR:", e)
        raise HTTPException(status_code=500, detail="Failed to retrieve user and bank details")