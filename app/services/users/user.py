from app.schemas.auth.request import RegisterUserRequest
from sqlalchemy.orm import Session
from app.sql.cruds import user as user_crud
from app.services.comman import CommonService


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.common_service = CommonService()

    def create_user(self, user: RegisterUserRequest):

        existing_user = user_crud.get_user(self.db, email=user.email)
        if existing_user:
            raise ValueError("User already exists")

        existing_user = user_crud.get_user(self.db, username=user.username)
        if existing_user:
            raise ValueError("User already exists")

        user.password = self.common_service.get_password_hash(user.password)

        user = user_crud.create_user(self.db, user.model_dump())

        return user
