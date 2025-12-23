from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from model.bank import BankDetails
from model.user import User
from Schemas.bank_schema import BankSchema
from Schemas.user_schema import UserSchema
from database import get_db
from utils.response_wrapper import api_response

router = APIRouter()

# BANK DETAILS

# Create Bank Details
@router.post("/bank/", response_model=dict)
def create_bank_details(bank: BankSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == bank.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    existing = db.query(BankDetails).filter(BankDetails.user_id == bank.user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bank details already exist for this user")
    try:
        db_bank = BankDetails(**bank.model_dump())
        db.add(db_bank)
        db.commit()
        db.refresh(db_bank)
        return api_response(data=BankSchema.model_validate(db_bank).model_dump(), message="Bank details created successfully")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create bank details")


# Get all Bank Details
@router.get("/bank/", response_model=dict)
def get_bank_details(db: Session = Depends(get_db)):
    db_banks = db.query(BankDetails).all()
    bank_list = [BankSchema.model_validate(bank).model_dump() for bank in db_banks]
    return api_response(data=bank_list, message="Bank details retrieved successfully")


# Update Bank Details by User ID
@router.put("/bank/{user_id}", response_model=dict)
def update_bank_details(user_id: int, bank: BankSchema, db: Session = Depends(get_db)):
    db_bank = db.query(BankDetails).filter(BankDetails.user_id == user_id).first()
    if not db_bank:
        raise HTTPException(status_code=404, detail="Bank details not found")

    for key, value in bank.model_dump(exclude_unset=True).items():
        setattr(db_bank, key, value)

    try:
        db.commit()
        db.refresh(db_bank)
        return api_response(
            data=BankSchema.model_validate(db_bank).model_dump(),
            message="Bank details updated successfully"
        )
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update bank details")


# Delete Bank Details by User ID
@router.delete("/bank/{user_id}", response_model=dict)
def delete_bank_details(user_id: int, db: Session = Depends(get_db)):
    db_bank = db.query(BankDetails).filter(BankDetails.user_id == user_id).first()
    if not db_bank:
        raise HTTPException(status_code=404, detail="Bank details not found")

    try:
        db.delete(db_bank)
        db.commit()
        return api_response(message="Bank details deleted successfully")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete bank details")


# USER DETAILS

# Create User
@router.post("/user/", response_model=dict)
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
@router.get("/user/{user_id}", response_model=dict)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return api_response(
        data=UserSchema.model_validate(db_user).model_dump(),
        message="User retrieved successfully"
    )


# Get all Users
@router.get("/users/", response_model=dict)
def get_all_users(db: Session = Depends(get_db)):
    db_users = db.query(User).all()
    user_list = [UserSchema.model_validate(user).model_dump() for user in db_users]
    return api_response(data=user_list, message="All users retrieved successfully")


# Update User by ID
@router.put("/user/{user_id}", response_model=dict)
def update_user(user_id: int, user: UserSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)

    try:
        db.commit()
        db.refresh(db_user)
        return api_response(
            data=UserSchema.model_validate(db_user).model_dump(),
            message="User updated successfully"
        )
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update user")


# Delete User by ID
@router.delete("/user/{user_id}", response_model=dict)
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
    

# Get User along with Bank Details by User ID

@router.get("/user/{user_id}/bank/", response_model=dict)
def get_user_bank_details(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    bank = db.query(BankDetails).filter(BankDetails.user_id == user_id).first()
    user_data = UserSchema.model_validate(user).model_dump()
    if bank:
        bank_data = BankSchema.model_validate(bank).model_dump()
    else:
        bank_data = {"user_id": user_id, "acc_num": None, "bank_nm": None}
    combined_data = {**user_data, **bank_data}
    return api_response(data=combined_data,message="User and bank details retrieved successfully")
   
   