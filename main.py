from fastapi import FastAPI
from database import Base, engine

from model.user import User
from model.bank import BankDetails

from routes.routes import router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router)