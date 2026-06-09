from pydantic import BaseModel
import typing as t


class CategoryCreateRequest(BaseModel):
    name: str
    user_id: t.Optional[int] = None


class CategoryUpdateRequest(BaseModel):
    name: t.Optional[str] = None
