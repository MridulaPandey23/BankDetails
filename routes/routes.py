from fastapi import APIRouter
from routes.userRoutes import router as user_router
from routes.bankRoutes import router as bank_router

router = APIRouter()
router.include_router(user_router)
router.include_router(bank_router)
