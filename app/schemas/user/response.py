from pydantic import BaseModel, EmailStr
import typing as t
from app.schemas.common_response import MetaDataResponse


class CurrentUserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    roles: t.List[str] = []
    created_at: t.Any

    class ConfigDict:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    roles: t.List[str] = []
    created_at: t.Any

    class ConfigDict:
        from_attributes = True


class UsersResponse(MetaDataResponse):
    users: t.List[UserResponse]

    class ConfigDict:
        from_attributes = True
