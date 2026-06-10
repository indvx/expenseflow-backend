from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
import typing as t
from app.db.dependencies import get_db
from app.services.users.user import UserService
from app.enums.role_enums import RoleFilterEnum
from app.core.security.auth import *
from app.schemas.user.response import *
from app.schemas.user.request import *
from fastapi.templating import Jinja2Templates
from datetime import datetime, UTC
from app.core.helper.mailer import Mailer

mailer = Mailer()
env = Jinja2Templates(directory="app/templates")

router = APIRouter(
    prefix="/users", tags=["Users"], responses={404: {"description": "Not Found"}}
)


def send_mail(user: AddNewUserRequest, inviter: t.Any):
    try:
        template = env.get_template("emails/invite-user.html.twig")
        html = template.render(
            member_name=user.username,
            invited_by=inviter.username,
            project_name="ExpenseFlow",
            invitation_url="http://localhost:8003/api/v1/auth/register",
            current_year=datetime.now(UTC).year,
        )
        mailer._send_mail(
            subject="Invitation to Join ExpenseFlow",
            to_email=user.email,
            body=html,
        )
        return True
    except Exception as e:
        print(e)
        return False


def send_password_reset_mail(user: t.Any, temp_password: str):
    try:
        template = env.get_template("emails/password-reset.html.twig")
        html = template.render(
            user_name=user.username,
            temp_password=temp_password,
            login_url="http://localhost:8003/api/v1/auth/login",
            current_year=datetime.now(UTC).year,
        )
        mailer._send_mail(
            subject="ExpenseFlow - Password Reset",
            to_email=user.email,
            body=html,
        )
        return True
    except Exception as e:
        print(e)
        return False


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
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    user_service = UserService(db)
    user = user_service.add_user(user_data)
    background_tasks.add_task(send_mail, user, d)
    return user


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


@router.post("/reset-password-request")
def reset_password_request(
    data: ResetPasswordRequest,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    user_service = UserService(db)
    user = user_service.password_reset_request(data.email)
    background_tasks.add_task(
        send_password_reset_mail, user["user"], user.get("temp_password")
    )

    return {"message": f"Reset password request sent for user {data.email}"}


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
