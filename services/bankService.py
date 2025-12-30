from sqlalchemy.ext.asyncio import AsyncSession
from model.bank import BankDetails

class BankService:
    async def create(db: AsyncSession, user_id: int, bank_data):
        bank = BankDetails(
            user_id=user_id,
            acc_num=bank_data.acc_num,
            bank_nm=bank_data.bank_nm
        )
        db.add(bank)
        return bank   