from fastapi import FastAPI
from database import Base, engine

from model.user import User
from model.bank import BankDetails

from Controllers.UserBank_controller import router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/api", tags=["UserBank"])

@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI CRUD API"}
