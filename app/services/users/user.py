from sqlalchemy.orm import Session
from app.sql.cruds import user as user_crud
from app.services.comman import CommonService


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.common_service = CommonService()

    def get_user(self, user_id):
        return user_crud.get_user(self.db, user_id=user_id)

