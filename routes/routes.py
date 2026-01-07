from fastapi import APIRouter
from routes.userRoutes import router as user_router
from routes.bankRoutes import router as bank_router
from routes.authRoutes import router as auth_router

router = APIRouter()
router.include_router(user_router)
router.include_router(bank_router)
router.include_router(auth_router)