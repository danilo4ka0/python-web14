from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from .models import User, UserInDB
from .dependencies import verify_email, rate_limit
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
users_db = {}

# Ліміт на створення контактів
limiter = Limiter(key_func=get_remote_address)

@router.post("/register")
@limiter.limit("5/minute")
async def register(email: EmailStr, password: str):
    """
    Реєстрація нового користувача.
    :param email: Email адреса користувача
    :param password: Пароль користувача
    :return: Повідомлення про успішну реєстрацію
    :raises HTTPException: Якщо користувач вже існує
    """
    if email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    user = User(email=email, password=password)
    users_db[email] = user
    # Логіка надсилання email з посиланням на верифікацію
    return {"msg": "Please verify your email"}

@router.get("/verify-email/{token}")
async def verify_email_route(token: str):
    """
    Верифікація електронної пошти користувача.
    :param token: Токен для верифікації
    :return: Повідомлення про успішну верифікацію
    :raises HTTPException: Якщо токен недійсний або користувач не знайдений
    """
    email = verify_email(token)
    if not email or email not in users_db:
        raise HTTPException(status_code=400, detail="Invalid verification token")
    users_db[email].is_verified = True
    return {"msg": "Email verified successfully"}
