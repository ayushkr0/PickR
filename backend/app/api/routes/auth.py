from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import create_token, get_current_user, hash_password, verify_password
from app.core.database import get_db
from app.models.user import User

router = APIRouter(prefix="/auth")


class RegisterRequest(BaseModel):
    email: str
    password: str
    display_name: str | None = None
    honeypot: str | None = None


class LoginRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    token: str
    user: "UserOut"


class UserOut(BaseModel):
    id: str
    email: str
    display_name: str | None
    is_admin: bool


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest, db: AsyncSession = Depends(get_db)):
    if body.honeypot:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Registration failed")

    if len(body.password) < 6:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Password must be at least 6 characters")

    existing = await db.execute(select(User).where(User.email == body.email.lower().strip()))
    if existing.scalar_one_or_none():
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered")

    user = User(
        email=body.email.lower().strip(),
        password_hash=hash_password(body.password),
        display_name=body.display_name,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return AuthResponse(
        token=create_token(user.id),
        user=UserOut(id=user.id, email=user.email, display_name=user.display_name, is_admin=user.is_admin),
    )


@router.post("/login", response_model=AuthResponse)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == body.email.lower().strip()))
    user = result.scalar_one_or_none()
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid email or password")

    return AuthResponse(
        token=create_token(user.id),
        user=UserOut(id=user.id, email=user.email, display_name=user.display_name, is_admin=user.is_admin),
    )


@router.get("/me", response_model=UserOut)
async def me(user: User = Depends(get_current_user)):
    return UserOut(id=user.id, email=user.email, display_name=user.display_name, is_admin=user.is_admin)
