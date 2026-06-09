from pydantic import BaseModel
from app.schemas.user.response import UserResponse
import typing as t
from app.schemas.common_response import MetaDataResponse


class CategoryResponse(BaseModel):
    id: int
    name: str
    user: UserResponse
    created_at: t.Any
    updated_at: t.Any

    class ConfigDict:
        from_attributes = True


class CategoriesResponse(MetaDataResponse):
    categories: t.List[CategoryResponse]

    class ConfigDict:
        from_attributes = True
