from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

from schemas.bank_schema import BankSchema
from schemas.user_schema import UserSchema
from controllers.userController import (create_user,get_user,get_all_users,update_user,delete_user)

router = APIRouter(prefix="/user", tags=["User"])


# ---------------- USER ROUTES ----------------

@router.post("/user/")
def add_user(user: UserSchema, db: Session = Depends(get_db)):
    return create_user(user, db)


@router.get("/user/{user_id}")
def fetch_user(user_id: int, db: Session = Depends(get_db)):
    return get_user(user_id, db)


@router.get("/")
def fetch_all_users(db: Session = Depends(get_db)):
    return get_all_users(db)


@router.put("/user/{id}")
def edit_user(user_id: int, user: UserSchema, db: Session = Depends(get_db)):
    return update_user(user_id, user, db)


@router.delete("/user/{user_id}")
def remove_user(user_id: int, db: Session = Depends(get_db)):
    return delete_user(user_id, db)
