from fastapi import APIRouter, Depends, status
import typing as t
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.core.security.auth import get_current_user
from app.sql.models.user import User
from app.schemas.category.request import CategoryCreateRequest, CategoryUpdateRequest
from app.schemas.category.response import CategoryResponse, CategoriesResponse
from app.services.category.category import CategoryService
from app.enums.category_enums import CategoryFilterEnum

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
    responses={404: {"description": "Not Found"}},
)


@router.get("", response_model=CategoriesResponse)
def get_categories(
    filter: t.Optional[str] = None,
    sort_by: t.Optional[str] = "id",
    order: t.Literal["asc", "desc"] = "desc",
    type: CategoryFilterEnum = CategoryFilterEnum.ALL,
    page: t.Optional[int] = 1,
    limit: t.Optional[int] = 20,
    start_date: t.Optional[str] = None,
    end_date: t.Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    category_service = CategoryService(db, current_user)
    return category_service.get_categories(
        filter=filter,
        sort_by=sort_by,
        order=order,
        category_type=type,
        page=page,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
    )


@router.post("", status_code=status.HTTP_201_CREATED, response_model=CategoryResponse)
def create_category(
    category: CategoryCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    category_service = CategoryService(db, current_user)
    return category_service.create_category(category)


@router.get("/{id:int}", response_model=CategoryResponse)
def get_category(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    category_service = CategoryService(db, current_user)
    return category_service.get_category(id)


@router.put("/{id:int}", response_model=CategoryResponse)
def update_category(
    id: int,
    category_data: CategoryUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    category_service = CategoryService(db, current_user)
    return category_service.update_category(id, category_data)


@router.delete("/{id:int}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    category_service = CategoryService(db, current_user)
    category_service.delete_category(id)
    return {"message": "Category deleted successfully"}
