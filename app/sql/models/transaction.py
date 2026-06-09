from app.db.base import Base
from sqlalchemy import Column, Float, Integer, String, DateTime, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from app.sql.models.category import Category
from app.sql.models.user import User
from app.enums.transaction_enums import TransactionEnum


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    transaction_date = Column(Date, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(Enum(TransactionEnum), nullable=False)
    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))

    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
