from fastapi import FastAPI
from database import Base, engine

from model.user import User
from model.bank import BankDetails

from routes.routes import router

app = FastAPI()

@app.on_event("startup")
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(router)
