from fastapi import APIRouter
from routes.user_routes import router as user_router
from routes.bank_routes import router as bank_router
from routes.auth_routes import router as auth_router

router = APIRouter()
router.include_router(user_router)
router.include_router(bank_router)
router.include_router(auth_router)