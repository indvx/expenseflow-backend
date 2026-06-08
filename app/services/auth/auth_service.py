from app.db.dependencies import get_db
from app.schemas.auth.request import LoginUserRequest, RegisterUserRequest
from app.services.users.user import UserService
from app.sql.cruds import user as user_crud
from app.services.comman import CommonService
from sqlalchemy.orm import Session
from fastapi import Depends
from app.sql.cruds import refresh_token as refresh_token_crud
from datetime import datetime, timedelta, timezone
import jwt
import uuid
import os
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()


class AuthService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.user_service = UserService(db)
        self.common_service = CommonService()

    def register(self, user: RegisterUserRequest):

        existing_user = user_crud.get_user(self.db, email=user.email)
        if existing_user:
            raise ValueError("User already exists")

        existing_user = user_crud.get_user(self.db, username=user.username)
        if existing_user:
            raise ValueError("User already exists")

        user.password = self.common_service.get_password_hash(user.password)

        user = user_crud.create_user(self.db, user.model_dump())

        return user

    def login(self, payload: LoginUserRequest):
        user = user_crud.get_user(self.db, email=payload.email)
        if not user:
            raise HTTPException(status_code=401, detail=("Invalid credentials"))

        valid_password = self.common_service.verify_password(
            payload.password, user.hashed_password
        )
        if not valid_password:
            raise HTTPException(status_code=401, detail=("Invalid password"))

        if not user.is_active:
            raise HTTPException(status_code=403, detail=("Your account is inactive"))

        access_token = self.common_service.create_jwt_token(user.id, type="access")
        refresh_data = self.common_service.create_jwt_token(user.id, type="refresh")

        refresh_token = refresh_token_crud.create_or_update_refresh_token(
            self.db,
            user_id=user.id,
            jti=refresh_data["jti"],
            token=refresh_data["token"],
            expires_at=refresh_data["expires_at"],
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token.token,
            "token_type": "bearer",
        }

    def refresh_token(self, refresh_token: str):
        payload = self.common_service.decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail=("Invalid token type"))

        jti = payload.get("jti")
        ref_token = refresh_token_crud.get_token_by_jti_or_user_id(self.db, jti=jti)
        if not ref_token:
            raise HTTPException(status_code=401, detail=("Token not found"))

        if ref_token.revoked:
            raise HTTPException(status_code=401, detail=("Token is revoked"))

        if refresh_token_crud.is_refresh_token_expired(ref_token):
            raise HTTPException(status_code=401, detail=("Token is expired"))

        access_token = self.common_service.create_jwt_token(
            ref_token.user_id, type="access"
        )
        return {"access_token": access_token, "token_type": "bearer"}

    def logout(self, user_id: int):
        refresh_token = refresh_token_crud.get_token_by_jti_or_user_id(
            self.db, user_id=user_id, revoked=False
        )
        refresh_token.revoked = True
        self.db.commit()
        self.db.refresh(refresh_token)

        return {"message": "Logged out successfully"}
