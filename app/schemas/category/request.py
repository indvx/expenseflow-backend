from pydantic import BaseModel
from app.enums.category_enums import CategoryType
import typing as t


class CategoryCreateRequest(BaseModel):
    name: str
    user_id: t.Optional[int] = None
    type: CategoryType


class CategoryUpdateRequest(BaseModel):
    name: t.Optional[str] = None
    type: t.Optional[CategoryType] = None
