from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from schemas.user_schema import UserSchema,BankSchema

async def create_user_with_bank(data: UserSchema,db: AsyncSession):
    try:
        user = user(name=data.name,age=data.age,gender=data.gender,email=data.email)
        db.add(user)
        await db.flush() 
        bank = BankSchema(user_id=user.id,acc_num=data.bank.acc_num,bank_nm=data.bank.bank_nm)
        db.add(bank)
        await db.commit()
        return {
            "user": {"id": user.id,"name": user.name,"age": user.age,"gender": user.gender,"email": user.email},
            "bank": {"acc_num": bank.acc_num,"bank_nm": bank.bank_nm}
        }
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))