from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import typing as t
from app.db.dependencies import get_db
from app.services.users.user import UserService
from app.enums.role_enums import RoleFilterEnum
from app.core.security.auth import *
from app.schemas.user.response import *
from app.schemas.user.request import *

router = APIRouter(
    prefix="/users", tags=["Users"], responses={404: {"description": "Not Found"}}
)


@router.get("/me", response_model=CurrentUserResponse)
def get_current_user(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    return current_user


@router.post("/add", response_model=UserResponse)
def add_new_user(
    user_data: AddNewUserRequest,
    db: Session = Depends(get_db),
    d: t.Any = Depends(has_roles(["admin"])),
):
    user_service = UserService(db)
    return user_service.add_user(user_data)


@router.put("/{id:int}", response_model=UserResponse)
def update_user(
    id: int,
    user_data: UserUpdateRequest,
    db: Session = Depends(get_db),
    d: t.Any = Depends(JWTBearer()),
):
    user_service = UserService(db)
    user = user_service.update_user(user_id=id, user_data=user_data)
    return user


@router.delete("/{id:int}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    id: int, db: Session = Depends(get_db), d: t.Any = Depends(JWTBearer())
):
    return {"message": f"Delete user {id}"}


@router.get("/{id:int}", response_model=CurrentUserResponse)
def get_user(id: int, db: Session = Depends(get_db), d: t.Any = Depends(JWTBearer())):
    user_service = UserService(db)
    return user_service.get_user(user_id=id)


@router.get("", response_model=UsersResponse)
def get_users_list(
    filter: t.Optional[str] = None,
    user_id: t.Optional[int] = None,
    status: t.Literal["all", "active", "inactive"] = "all",
    limit: t.Optional[int] = 10,
    page: t.Optional[int] = 1,
    role: RoleFilterEnum = RoleFilterEnum.ALL,
    sort_by: t.Optional[str] = "id",
    order: t.Literal["asc", "desc"] = "desc",
    start_date: t.Optional[str] = None,
    end_date: t.Optional[str] = None,
    db: Session = Depends(get_db),
    d: t.Any = Depends(JWTBearer()),
):
    user_service = UserService(db)
    return user_service.get_users(
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
