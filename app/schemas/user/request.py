from pydantic import BaseModel, EmailStr, Field
import typing as t
from app.enums.role_enums import RoleEnum


class UserUpdateRequest(BaseModel):
    username: t.Optional[str] = None
    email: t.Optional[EmailStr] = None
    is_active: t.Optional[bool] = None


class AddNewUserRequest(UserUpdateRequest):
    roles: t.List[RoleEnum] = [RoleEnum.GUEST]
