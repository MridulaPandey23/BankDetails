from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

from schemas.bank_schema import BankSchema
from schemas.user_schema import UserSchema

from controllers.bankController import (create_bank_details,get_bank_details,get_bank,update_bank_details,delete_bank_details,get_user_bank_details)

router = APIRouter(prefix="/bank", tags=["Bank"])

# ---------------- BANK ROUTES ----------------

@router.post("/bank/")
def create_bank(bank: BankSchema, db: Session = Depends(get_db)):
    return create_bank_details(bank, db)


@router.get("/bank/")
def get_all_banks(db: Session = Depends(get_db)):
    return get_bank_details(db)

@router.get("/user/{user_id}")
def fetch_user(bank_id: int, db: Session = Depends(get_db)):
    return get_bank(bank_id, db)

@router.put("/bank/{id}")
def update_bank(id: int, bank: BankSchema, db: Session = Depends(get_db)):
    return update_bank_details(id, bank, db)

@router.delete("/bank/{id}")
def delete_bank(id: int, db: Session = Depends(get_db)):
    return delete_bank_details(id, db)


# -------- USER + BANK COMBINED --------

@router.get("/userbank/{user_id}")
def fetch_user_bank(user_id: int, db: Session = Depends(get_db)):
    return get_user_bank_details(user_id, db)
