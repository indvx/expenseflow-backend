from app.sql.models.user import User
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc


def create_user(db: Session, user: dict):
    user_data = User()
    user_data.username = user.get("username")
    user_data.email = user.get("email")
    user_data.hashed_password = user.get("password")
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


