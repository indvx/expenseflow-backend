from pwdlib import PasswordHash
import jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone
import uuid
from fastapi import HTTPException

load_dotenv()


class CommonService:
    def __init__(self):
        self.password_hash = PasswordHash.recommended()
        self.secret_key = os.getenv("SECRET_KEY")
        self.algorithm = os.getenv("ALGORITHM", "HS256")
        self.access_token_expire_minutes = int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15)
        )
        self.refresh_token_expire_days = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

    def verify_password(self, plain_password: str, hashed_password: str):
        return self.password_hash.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        return self.password_hash.hash(password)

    def create_jwt_token(self, user_id: int, type: str = "access"):
        if type == "access":
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=self.access_token_expire_minutes
            )
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                days=self.refresh_token_expire_days
            )

        jti = str(uuid.uuid4())
        payload = {
            "sub": str(user_id),
            "type": type,
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "jti": jti,
        }

        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        if type == "access":
            return token

        return {"token": token, "jti": jti, "expires_at": expire}

    def decode_token(self, token: str):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail=("Token expired"))

        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail=("Invalid token"))
