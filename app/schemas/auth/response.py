from pydantic import BaseModel
import typing as t


class RegisterResponse(BaseModel):
    id: int
    username: str
    email: str
    roles: t.List[str]
    created_at: t.Any
    updated_at: t.Any

    class ConfigDict:
        from_attributes = True
        populate_by_name = True


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenResponse(BaseModel):
    access_token: str
    token_type: str

    class ConfigDict:
        from_attributes = True
        populate_by_name = True
