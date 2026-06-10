from sqlalchemy.orm import Session
from app.sql.models.category import Category
from app.schemas.category.request import CategoryCreateRequest
from sqlalchemy import desc, asc
from datetime import datetime, timedelta, date, UTC


def create_category(db: Session, category_data: dict):
    category = Category()
    category.name = category_data.get("name")
    category.user_id = category_data.get("user_id")
    category.type = category_data.get("type")
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_category_by_id(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()


def update_category(db: Session, category: Category, category_data: dict):

    if "name" in category_data and category_data["name"] != "":
        category.name = category_data["name"]

    if "type" in category_data and category_data["type"] != "":
        category.type = category_data["type"]

    if "user_id" in category_data and category_data["user_id"] != "":
        category.user_id = category_data["user_id"]

    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category: Category):
    db.delete(category)
    db.commit()
    return True


def get_categories(
    db: Session,
    filter: str = None,
    user_id: int = None,
    limit: int = 10,
    page: int = 1,
    sort_by: str = "id",
    order: str = "desc",
    start_date: str = None,
    end_date: str = None,
):
    query = db.query(Category)

    if filter and filter != "":
        filter_by = f"%{filter.strip()}%"
        query = query.filter(Category.name.like(filter_by))

    if user_id and user_id != 0:
        query = query.filter(Category.user_id == user_id)

    if order != "" and sort_by != "":
        if order == "desc":
            query = query.order_by(desc(getattr(Category, sort_by)))
        elif order == "asc":
            query = query.order_by(asc(getattr(Category, sort_by)))

    if start_date is not None:
        if end_date is None:
            end_date = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
        else:
            end_date = end_date + timedelta(days=1) - timedelta(seconds=1)

        query = query.filter(Category.created_at >= start_date).filter(
            Category.created_at <= end_date
        )

    total_items = query.count()

    if limit and limit != 0:
        query = query.limit(limit)
        offset = (int(page) - 1) * limit
        query = query.offset(offset)

    categories = query.all()

    return {
        "limit": limit,
        "page": page,
        "total_items": total_items,
        "item": len(categories),
        "categories": categories,
    }
