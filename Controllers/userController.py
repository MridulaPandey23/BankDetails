from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from model.user import User
from schemas.user_schema import UserSchema
from database import get_async_db
from utils.response_wrapper import api_response
from sqlalchemy import text, select


# Create User

async def create_user(user: UserSchema, db: AsyncSession = Depends(get_async_db)):
    try: 
        query = text("INSERT INTO user_details (name, age, gender, email) VALUES (:name,:age, :gender, :email) RETURNING id, name, age, gender, email")
        result = await db.execute(query, {"name": user.name, "age": user.age, "gender": user.gender, "email": user.email})
        await db.commit()
        row = result.mappings().one()
        return api_response([{"id": row["id"],"name": row["name"], "age": row["age"], "gender": row["gender"], "email": row["email"]}], message = " User added successfully")
    except Exception as e:
        print("GENERAL ERROR:", e)
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create user details")

# Get User by ID

async def get_user(user_id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        query = text("Select id, name, age, email, gender from user_details where id = :id ")
        result = await db.execute(query, {"id": user_id})
        row = result.mappings().first()
        if not row:
            raise HTTPException(status_code=404, detail="User not found")
        data = [{ "id": row["id"], "name": row["name"],"gender": row["gender"],"email": row["email"], "age": row["age"] }]
        return api_response(data=data, message="Users retrieved successfully")
    except Exception as e:
        print("GENERAL ERROR:", e)
        raise HTTPException(status_code=500, detail="Failed to retrieve users")

# Get all Users

async def get_all_users(db: AsyncSession = Depends(get_async_db)):
    try:
        query = text("SELECT * FROM user_details")
        result = await db.execute(query)
        rows = result.mappings().all()
        data = [{ "id": row["id"], "name": row["name"],"gender": row["gender"],"email": row["email"], "age": row["age"] } for row in rows]
        return api_response(data=data, message="Users retrieved successfully")
    except Exception as e:
        print("GENERAL ERROR:", e)
        raise HTTPException(status_code=500, detail="Failed to retrieve users")

# Update User by ID

async def update_user(user_id: int, user: UserSchema, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    existing = result.scalar_one_or_none()
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        query = text("UPDATE user_details SET name = :name, age = :age, gender = :gender, email = :email WHERE id = :id RETURNING id, name, age, gender, email")
        result = await db.execute(query, {"id": user_id,"name": user.name,"age": user.age,"gender": user.gender,"email": user.email})
        await db.commit()
        row = result.mappings().one()
        return api_response(data=[{"id": row["id"],"name": row["name"],"age": row["age"],"gender": row["gender"],"email": row["email"]}],message="User details updated successfully")
    except Exception as e:
        print("GENERAL ERROR:", e)
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update user details")



# Delete User by ID
async def delete_user(user_id: int, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        query = text("DELETE from user_details Where id = :id")
        await db.execute(query, {"id": user_id})
        await db.commit()
        return api_response(message="User details deleted successfully")
    except Exception as e:
        print("GENERAL ERROR:", e)
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete user details")  

   
   