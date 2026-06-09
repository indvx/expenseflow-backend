from app.sql.models.user import User
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
import typing as t
from datetime import datetime, timedelta, UTC


def create_user(db: Session, user: dict):
    user_data = User()
    user_data.username = user.get("username")
    user_data.email = user.get("email")
    user_data.hashed_password = user.get("password")
    user_data.roles = user.get("roles")
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return user_data


def get_user(db: Session, user_id: int = None, username: str = None, email: str = None):
    query = db.query(User)
    if user_id:
        query = query.filter(User.id == user_id)
    elif username:
        query = query.filter(User.username == username)
    elif email:
        query = query.filter(User.email == email)
    return query.first()


def update_user(db: Session, user: User, user_data: dict):
    if "username" in user_data and user_data["username"] != "":
        user.username = user_data["username"]
    if "email" in user_data and user_data["email"] != "":
        user.email = user_data["email"]
    if "is_active" in user_data and user_data["is_active"] is not None:
        user.is_active = user_data["is_active"]
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_roles(db: Session, user: User, roles: t.List[str] = []):
    pass


def get_users(
    db: Session,
    filter: str = None,
    user_id: int = None,
    status: str = None,
    limit: int = 10,
    page: int = 1,
    sort_by: str = "id",
    order: str = "desc",
    start_date: str = None,
    end_date: str = None,
    role: str = None,
):
    query = db.query(User)
    if filter and filter is not None and filter != "":
        filter_by = f"%{filter.strip()}%"

        query = query.filter(User.email.like(filter_by) | User.username.like(filter_by))

    if status and status != "all":
        if status == "active":
            query = query.filter(User.is_active == True)
        else:
            query = query.filter(User.is_active == False)

    if user_id and user_id != 0:
        query = query.filter(User.id == user_id)

    if role and role != "all":
        query = query.filter(User.roles.any(role))

    if order != "" and sort_by != "":
        if order == "desc":
            query = query.order_by(desc(getattr(User, sort_by)))
        elif order == "asc":
            query = query.order_by(asc(getattr(User, sort_by)))

    if start_date is not None:
        if end_date is None:
            end_date = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
        else:
            end_date = end_date + timedelta(days=1) - timedelta(seconds=1)

        query = query.filter(User.created_at >= start_date).filter(
            User.created_at <= end_date
        )

    total_items = query.count()

    if limit and limit != 0:
        query = query.limit(limit)
        offset = (int(page) - 1) * limit
        query = query.offset(offset)

    users = query.all()

    return {
        "limit": limit,
        "page": page,
        "total_items": total_items,
        "item": len(users),
        "users": users,
    }
