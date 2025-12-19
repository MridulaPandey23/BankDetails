from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from model import BankDetails

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/")
def add_bank_details(acc_num: int, bank_nm: str, db: Session = Depends(get_db)):
    bank_detail = BankDetails(acc_num=acc_num, bank_nm=bank_nm)
    existing_acc = db.query(BankDetails).filter(BankDetails.acc_num == acc_num).first()
    if existing_acc:
        raise HTTPException(status_code=400, detail="Account number already exists")
    db.add(bank_detail)
    db.commit()
    db.refresh(bank_detail)
    return JSONResponse(status_code=201, content={"acc_num": bank_detail.acc_num, "bank_nm": bank_detail.bank_nm})

@app.put("/")
def update_bank_details(acc_num: int, bank_nm: str, db: Session = Depends(get_db)):
    bank_detail = db.query(BankDetails).filter(BankDetails.acc_num == acc_num).first()
    if not bank_detail:
        raise HTTPException(status_code=404, detail="Bank details not found")
    bank_detail.bank_nm = bank_nm
    db.commit()
    db.refresh(bank_detail)
    return bank_detail

@app.delete("/{acc_num}")
def delete_bank_details(acc_num: int, db: Session = Depends(get_db)):
    bank_detail = db.query(BankDetails).filter(BankDetails.acc_num == acc_num).first()
    if not bank_detail:
        raise HTTPException(status_code=404, detail="Bank details not found")
    db.delete(bank_detail)
    db.commit()
    return JSONResponse(status_code=200, content={"detail": "Bank details deleted successfully"})

@app.get("/{acc_num}")
def get_bank_details(acc_num: int, db: Session = Depends(get_db)):
    bank_detail = db.query(BankDetails).filter(BankDetails.acc_num == acc_num).first()
    if not bank_detail:
        raise HTTPException(status_code=404, detail="Bank details not found")
    return JSONResponse(status_code=200, content={"acc_num": bank_detail.acc_num, "bank_nm": bank_detail.bank_nm})