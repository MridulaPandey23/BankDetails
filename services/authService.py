from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
import uuid

from utils.security import hash_password, verify_password, create_jwt_token
from utils.mail import send_set_password_email

async def register_user(name: str, email: str, db: AsyncSession):
    result = await db.execute(text("SELECT id FROM user_details WHERE email = :email"),{"email": email})
    if result.first():
        raise HTTPException(status_code=400, detail="Email already exists")
    user_result = await db.execute(text("INSERT INTO user_details (name, email, password, isverified) VALUES (:name, :email, NULL, FALSE)RETURNING id"),
        {"name": name, "email": email})
    user_id = user_result.scalar()
    token = str(uuid.uuid4())
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=30)
    await db.execute(text("INSERT INTO password_tokens (user_id, token, expires_at, is_used) VALUES (:user_id, :token, :expires_at, FALSE)"),
        {"user_id": user_id, "token": token, "expires_at": expires_at})
    await db.commit()
    await send_set_password_email(email, token)
    return {"message": "Registration successful. Check your email to set password"}

async def set_password(token: str, new_password: str, db: AsyncSession):
    result = await db.execute(text("SELECT user_id, expires_at, is_used FROM password_tokens WHERE token = :token"),{"token": token})
    token_data = result.mappings().first()
    if not token_data:
        raise HTTPException(status_code=400, detail="Invalid token")
    if token_data["is_used"]:
        raise HTTPException(status_code=400, detail="Token already used")
    now = datetime.now(timezone.utc)
    if token_data["expires_at"] < now:
        raise HTTPException(status_code=400, detail="Token expired")
    hashed_password = hash_password(new_password)
    await db.execute(text("UPDATE user_details SET password = :password, isVerified = TRUE WHERE id = :user_id"),
        {"password": hashed_password, "user_id": token_data["user_id"]})
    await db.execute(text("UPDATE password_tokens SET is_used = TRUE WHERE token = :token"),
        {"token": token})
    await db.commit()
    return {"message": "Password set successfully"}

async def login_user(email: str, password: str, db: AsyncSession):
    result = await db.execute(text("SELECT id, password, isVerified FROM user_details WHERE email = :email"),{"email": email})
    user = result.mappings().first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not user["isverified"]:
        raise HTTPException(status_code=403, detail="Please verify your account")
    if not verify_password(password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_jwt_token({"user_id": user["id"]})
    return {"access_token": token, "token_type": "bearer"}
