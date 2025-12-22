from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal
from sqlalchemy import text
from model import BankDetails,User

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Bank Details CRUD Operations

@app.get("/bank")
def get_bank_details(db: Session = Depends(get_db)):
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    query = db.execute(text("SELECT * FROM bank_details"))
    row = query.mappings().all()
    return row

@app.get("/{user_id}")
def get_bank_details(user_id: int, db: Session = Depends(get_db)):
    row = db.execute(text("SELECT * FROM bank_details WHERE user_id = :user_id"), {"user_id": user_id}).mappings().first()
    if row is None:
        raise HTTPException(status_code=404, detail="Bank details not found")
    return row

@app.get("/bank/user/{user_id}")
def get_user_bank_details(user_id: int, db: Session = Depends(get_db)):
    row = db.execute(text("Select user_details.id, user_details.name, user_details.age, user_details.email,bank_details.acc_num, bank_details.bank_nm From user_details " \
    "left JOIN bank_details ON user_details.id = bank_details.user_id WHERE user_details.id = :user_id"), {"user_id": user_id}).mappings().first()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    if row is None:
        raise HTTPException(status_code=404, detail="User bank details not found")
    return row


@app.post("/bank")
def insert_bank_detail(user_id: int, acc_num: int, bank_nm: str, db: Session = Depends(get_db)):
    existing = db.query(BankDetails).filter(BankDetails.acc_num == acc_num).first()
    if existing:
        raise HTTPException(status_code=400, detail="Account number already exists")
    id_existing = db.query(BankDetails).filter(User.id == user_id).first()
    if not id_existing:
        raise HTTPException(status_code=404, detail="User ID does not exist")
    db.execute(text("INSERT INTO bank_details (user_id, acc_num, bank_nm)VALUES (:user_id, :acc_num, :bank_nm)"),{"user_id": user_id,"acc_num": acc_num,"bank_nm": bank_nm})
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Inserted"})

@app.put("/{user_id}")
def update_bank_detail(user_id: int, acc_num: int, bank_nm: str, db: Session = Depends(get_db)):
    existing = db.query(BankDetails).filter(BankDetails.user_id == user_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Bank details not found")
    db.execute(text("UPDATE bank_details SET acc_num=:acc_num, bank_nm=:bank_nm WHERE user_id=:user_id"),{"user_id": user_id, "acc_num": acc_num, "bank_nm": bank_nm})
    db.commit()
    return JSONResponse(status_code=200, content={"user_id": user_id, "acc_num": acc_num, "bank_nm": bank_nm})

@app.delete("/{user_id}")
def delete_bank_detail(user_id: int, db: Session = Depends(get_db)):
    existing = db.query(BankDetails).filter(BankDetails.user_id == user_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Bank details not found")
    query = text("DELETE from bank_details Where user_id = :user_id")
    db.execute(query, {"user_id": user_id})
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Deleted"})


# User Details CRUD Operations

@app.post("/")
def add_user_details(name: str, age: int, gender: str, email: str, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    db.execute(text("INSERT INTO user_details (name, age, gender, email)VALUES (:name, :age, :gender, :email)"),{"name": name,"age": age,"gender": gender,"email": email})
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Inserted"})

@app.put("/")
def update_user_details(id: int, name: str, age: int, gender: str, email: str, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.id == id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="No such user present")
    db.execute(text("UPDATE user_details SET name=:name, age=:age, gender=:gender, email=:email WHERE id=:id"),{"id": id, "name": name, "age": age, "gender": gender, "email": email})
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Updated successfully"})

@app.delete("/{id}")
def delete_user_details(id: int, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.id == id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="No such user present")
    query = text("DELETE from user_details Where id = :id")
    db.execute(query, {"id": id})
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Deleted"})   

@app.get("/{id}")
def get_user_details(id: int, db: Session = Depends(get_db)):
    row = db.execute(text("SELECT * FROM user_details WHERE id = :id"), {"id": id}).mappings().first()
    if row is None:
        raise HTTPException(status_code=404, detail="User not found")
    return row 
