from sqlalchemy.orm import Session
from app.sql.models.transaction import Transaction
from app.sql.models.user import User
from app.sql.models.category import Category
from sqlalchemy import or_, desc, asc, String, extract, func
from datetime import date
from app.enums.transaction_enums import TransactionEnum


def create_transaction(db: Session, transaction: dict):
    db_transaction = Transaction()
    db_transaction.amount = transaction.get("amount")
    db_transaction.description = transaction.get("description")
    db_transaction.transaction_date = transaction.get("transaction_date", date.today())
    db_transaction.category_id = transaction.get("category_id")
    db_transaction.type = transaction.get("type")
    db_transaction.user_id = transaction.get("user_id")
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_transaction_by_id(db: Session, transaction_id: int):
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()


def update_transaction(db: Session, transaction: Transaction, transaction_data: dict):
    if "amount" in transaction_data:
        transaction.amount = transaction_data["amount"]
    if "description" in transaction_data and transaction_data["description"] != "":
        transaction.description = transaction_data["description"]
    if (
        "transaction_date" in transaction_data
        and transaction_data["transaction_date"] != ""
    ):
        transaction.transaction_date = transaction_data["transaction_date"]
    if "category_id" in transaction_data and transaction_data["category_id"] != 0:
        transaction.category_id = transaction_data["category_id"]
    if "type" in transaction_data and transaction_data["type"] != "":
        transaction.type = transaction_data["type"]
    if "user_id" in transaction_data and transaction_data["user_id"] != 0:
        transaction.user_id = transaction_data["user_id"]
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


def delete_transaction(db: Session, transaction: Transaction) -> bool:
    db.delete(transaction)
    db.commit()
    return True


def get_transactions(
    db: Session,
    filter: str = None,
    user_id: int = None,
    category_id: int = None,
    transaction_type: str = None,
    limit: int = 10,
    page: int = 1,
    sort_by: str = "id",
    order: str = "desc",
    start_date: str = None,
    end_date: str = None,
    min_amount: float = None,
    max_amount: float = None,
) -> dict:
    query = db.query(Transaction)

    if filter and filter != "":
        filter_by = f"%{filter.strip()}%"
        query = query.filter(
            or_(
                Transaction.description.like(filter_by),
                Transaction.amount.cast(String).like(filter_by),
                Transaction.category.has(Category.name.like(filter_by)),
                Transaction.user.has(User.username.like(filter_by)),
                Transaction.user.has(User.email.like(filter_by)),
            )
        )

    if user_id and user_id != 0:
        query = query.filter(Transaction.user_id == user_id)

    if category_id and category_id != 0:
        query = query.filter(Transaction.category_id == category_id)

    if transaction_type and transaction_type != "all" and transaction_type != "":
        query = query.filter(Transaction.type == transaction_type.upper())

    if min_amount and min_amount != 0:
        query = query.filter(Transaction.amount >= min_amount)

    if max_amount and max_amount != 0:
        query = query.filter(Transaction.amount <= max_amount)

    if order != "" and sort_by != "":
        if order == "desc":
            query = query.order_by(desc(getattr(Transaction, sort_by)))
        elif order == "asc":
            query = query.order_by(asc(getattr(Transaction, sort_by)))

    if start_date is not None:
        if end_date is None:
            end_date = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
        else:
            end_date = end_date + timedelta(days=1) - timedelta(seconds=1)

        query = query.filter(Transaction.transaction_date >= start_date).filter(
            Transaction.transaction_date <= end_date
        )

    total_items = query.count()
    if limit and limit != 0:
        query = query.limit(limit)
        offset = (int(page) - 1) * limit
        query = query.offset(offset)

    transactions = query.all()

    return {
        "limit": limit,
        "page": page,
        "total_items": total_items,
        "item": len(transactions),
        "transactions": transactions,
    }

