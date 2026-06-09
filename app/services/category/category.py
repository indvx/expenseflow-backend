from sqlalchemy.orm import Session
from fastapi import Depends
from app.schemas.category.request import CategoryCreateRequest, CategoryUpdateRequest
from app.core.security.auth import get_current_user
from app.sql.cruds import category as category_crud
from app.core.exceptions.exceptions import NotFoundException, ForbiddenException
import typing as t
from app.enums.role_enums import RoleEnum
from datetime import datetime


class CategoryService:
    def __init__(self, db: Session, user: t.Any = Depends(get_current_user)):
        self.db = db
        self.logged_user = user

    def create_category(self, category: CategoryCreateRequest):
        if isinstance(category.user_id, int) and category.user_id != 0:
            if (
                RoleEnum.ADMIN not in self.logged_user.roles
                and category.user_id != self.logged_user.id
            ):
                raise ForbiddenException(
                    "You are not authorized to create category for another user"
                )
        else:
            category.user_id = self.logged_user.id

        result = category_crud.create_category(self.db, category.model_dump())
        return result

    def get_category(self, id: int):
        category = category_crud.get_category_by_id(self.db, id)
        if category is None:
            raise NotFoundException("Category not found")
        return category

    def update_category(self, id: int, category_data: CategoryUpdateRequest):
        category = self.get_category(id)
        if (
            category.user_id != self.logged_user.id
            and RoleEnum.ADMIN not in self.logged_user.roles
        ):
            raise ForbiddenException("You are not authorized to update this category")

        return category_crud.update_category(
            self.db, category=category, category_data=category_data.model_dump()
        )

    def delete_category(self, id: int):
        category = self.get_category(id)

        if (
            category.user_id != self.logged_user.id
            and RoleEnum.ADMIN not in self.logged_user.roles
        ):
            raise ForbiddenException("You are not authorized to delete this category")

        return category_crud.delete_category(self.db, category)

    def get_categories(
        self,
        filter: t.Optional[str] = None,
        user_id: t.Optional[int] = None,
        limit: int = 10,
        page: int = 1,
        sort_by: str = "id",
        order: str = "desc",
        start_date: t.Optional[str] = None,
        end_date: t.Optional[str] = None,
        category_type: str = "all",
    ):
        if start_date:
            if start_date != "":
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date:
            if end_date != "":
                end_date = datetime.strptime(end_date, "%Y-%m-%d")

        return category_crud.get_categories(
            self.db,
            filter=filter,
            user_id=user_id,
            limit=limit,
            page=page,
            sort_by=sort_by,
            order=order,
            start_date=start_date,
            end_date=end_date,
            category_type=category_type,
        )
