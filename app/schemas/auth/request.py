from pydantic import BaseModel, EmailStr, field_validator, ValidationInfo, Field


class RegisterUserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=16)
    confirm_password: str = Field(min_length=8)

    @field_validator("password")
    def password_complexity(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not any(c in "!@#$%^&*()" for c in v):
            raise ValueError("Password must contain at least one special character")
        return v

    @field_validator("confirm_password")
    def password_match(cls, v, info: ValidationInfo):
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Passwords do not match")
        return v
