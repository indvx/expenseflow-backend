from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.auth.request import RegisterUserRequest
from fastapi import status
from app.db.dependencies import get_db
from app.services.users.user import UserService

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Not Found"},
    },
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: RegisterUserRequest, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user = user_service.create_user(user)
    return user


@router.post("/login")
def login():
    pass


@router.post("/refresh")
def refresh():
    pass


@router.post("/logout")
def logout():
    pass
