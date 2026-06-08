from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.auth.request import (
    RegisterUserRequest,
    LoginUserRequest,
    RefreshTokenRequest,
)
from fastapi import status
from app.db.dependencies import get_db
from app.services.auth.auth_service import AuthService
from app.core.security import *
import typing as t

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Not Found"},
    },
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: RegisterUserRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    user = auth_service.register(user)
    return user


@router.post("/login")
def login(user: LoginUserRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.login(user)


@router.post("/refresh")
def refresh(token: RefreshTokenRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.refresh_token(token.refresh_token)


@router.post("/logout")
def logout(d: t.Any = Depends(get_current_user), db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.logout(d.id)
