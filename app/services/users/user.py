from sqlalchemy.orm import Session
from app.sql.cruds import user as user_crud
from app.services.comman import CommonService
from app.schemas.user.request import UserUpdateRequest, AddNewUserRequest
from app.core.exceptions.exceptions import NotFoundException, AlreadyExistsException


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.common_service = CommonService()

    def get_user(self, user_id):
        user = user_crud.get_user(self.db, user_id=user_id)
        if not user:
            raise NotFoundException(message="Provided user detail not found")
        return user

    def update_user(self, user_id, user_data: UserUpdateRequest):
        user = self.get_user(user_id)
        data = user_data.model_dump(exclude_unset=True)

        user = user_crud.update_user(self.db, user, data)

        return user

    def add_user(self, user_data: AddNewUserRequest):
        existing_user = user_crud.get_user(self.db, email=user_data.email)
        if existing_user:
            raise AlreadyExistsException(field="email")

        existing_user = user_crud.get_user(self.db, username=user_data.username)
        if existing_user:
            raise AlreadyExistsException(field="username")

        data = user_data.model_dump(exclude_unset=True)
        data["password"] = self.common_service.get_password_hash("Password1!")

        user = user_crud.create_user(self.db, data)

        return user

    def get_users(
        self,
        filter: str = None,
        user_id: int = None,
        status: str = None,
        role: str = None,
        limit: int = 10,
        page: int = 1,
        sort_by: str = "id",
        order: str = "desc",
        start_date: str = None,
        end_date: str = None,
    ):
        return user_crud.get_users(
            self.db,
            filter=filter,
            user_id=user_id,
            status=status,
            limit=limit,
            page=page,
            role=role,
            sort_by=sort_by,
            order=order,
            start_date=start_date,
            end_date=end_date,
        )
