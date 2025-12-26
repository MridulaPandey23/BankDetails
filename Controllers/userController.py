from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from model.user import User
from schemas.user_schema import UserSchema
from database import get_db
from utils.response_wrapper import api_response
from sqlalchemy import text


# Create User

def create_user(user: UserSchema, db: Session = Depends(get_db)):
    try:
        db_user = User(**user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return api_response(
            data=UserSchema.model_validate(db_user).model_dump(),
            message="User created successfully"
        )
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create user")


# Get User by ID

def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        query = text("Select id, name, age, email, gender from user_details where id = :id ")
        result = db.execute(query, {"id": user_id})
        row = result.fetchone()
        data = [{ "id": row.id, "name": row.name,"gender": row.gender,"email": row.email, "age": row.age }]
        return api_response(data=data, message="Users retrieved successfully")
    except Exception as e:
        print("GENERAL ERROR:", e)
        raise HTTPException(status_code=500, detail="Failed to retrieve users")

# Get all Users

def get_all_users(db: Session = Depends(get_db)):
    try:
        query = text("SELECT * FROM user_details")
        result = db.execute(query)
        rows = result.fetchall()
        data = [{ "id": row.id, "name": row.name,"gender": row.gender,"email": row.email, "age": row.age } for row in rows]
        return api_response(data=data, message="Users retrieved successfully")
    except Exception as e:
        print("GENERAL ERROR:", e)
        raise HTTPException(status_code=500, detail="Failed to retrieve users")

# Update User by ID

def update_user(user_id: int, user: UserSchema, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.id == user_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        query = text("UPDATE user_details SET name = :name, age = :age, gender = :gender, email = :email WHERE id = :id RETURNING id, name, age, gender, email")
        result = db.execute(query, {"id": user_id,"name": user.name,"age": user.age,"gender": user.gender,"email": user.email})
        db.commit()
        row = result.fetchone()
        return api_response(data={"id": row.id,"name": row.name,"age": row.age,"gender": row.gender,"email": row.email},message="User details updated successfully")
    except Exception as e:
        print("GENERAL ERROR:", e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update user details")



# Delete User by ID
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        db.delete(db_user)
        db.commit()
        return api_response(message="User deleted successfully")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete user")
   
   