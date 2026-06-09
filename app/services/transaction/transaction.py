from sqlalchemy.orm import Session
from app.sql.cruds import (
    transaction as transaction_crud,
    category as category_crud,
    user as user_crud,
)
from app.services.comman import CommonService
from app.schemas.transaction.request import (
    TransactionCreateRequest,
    TransactionUpdateRequest,
)
from fastapi import Depends
from app.core.security.auth import get_current_user
from app.enums.role_enums import RoleEnum
from app.core.exceptions.exceptions import NotFoundException, ForbiddenException
from datetime import datetime, UTC


class TransactionService:
    def __init__(self, db: Session, user=Depends(get_current_user)):
        self.db = db
        self.common_service = CommonService()
        self.logged_user = user

    def create_transaction(self, transaction: TransactionCreateRequest):
        category_exists = category_crud.get_category_by_id(
            self.db, transaction.category_id
        )
        if not category_exists:
            raise NotFoundException(message="Provided category details not found")

        user_id = self.logged_user.id
        if (
            hasattr(transaction, "user_id")
            and transaction.user_id != 0
            and transaction.user_id != user_id
        ):
            if RoleEnum.ADMIN in self.logged_user.roles:
                user_id = transaction.user_id
            else:
                raise ForbiddenException(
                    message="You are not authorized to create transaction for other user"
                )

        if not user_crud.check_user_exists(self.db, user_id):
            raise NotFoundException(message="Provided user details not found")

        data = transaction.model_dump(exclude_unset=True)
        data["user_id"] = user_id
        transaction = transaction_crud.create_transaction(self.db, data)
        return transaction

    def get_transaction(self, transaction_id: int):
        transaction = transaction_crud.get_transaction_by_id(self.db, transaction_id)
        if not transaction:
            raise NotFoundException(message="Provided transaction details not found")
        return transaction

    def update_transaction(
        self, transaction_id: int, transaction: TransactionUpdateRequest
    ):

        transaction_exists = transaction_crud.get_transaction_by_id(
            self.db, transaction_id
        )
        if not transaction_exists:
            raise NotFoundException(message="Provided transaction details not found")

        category_exists = category_crud.get_category_by_id(
            self.db, transaction.category_id
        )
        if not category_exists:
            raise NotFoundException(message="Provided category details not found")

        user_id = self.logged_user.id
        if (
            hasattr(transaction, "user_id")
            and transaction.user_id != 0
            and transaction.user_id != user_id
        ):
            if RoleEnum.ADMIN in self.logged_user.roles:
                user_id = transaction.user_id
            else:
                raise ForbiddenException(
                    message="You are not authorized to update transaction for other user"
                )

        if not user_crud.check_user_exists(self.db, user_id):
            raise NotFoundException(message="Provided user details not found")

        data = transaction.model_dump(exclude_unset=True)
        data["user_id"] = user_id
        transaction = transaction_crud.update_transaction(
            self.db, transaction_exists, data
        )
        return transaction

    def delete_transaction(self, transaction_id: int):
        transaction = transaction_crud.get_transaction_by_id(self.db, transaction_id)
        if not transaction:
            raise NotFoundException(message="Provided transaction details not found")

        if transaction.user_id != self.logged_user.id:
            if RoleEnum.ADMIN not in self.logged_user.roles:
                raise ForbiddenException(
                    message="You are not authorized to delete transaction for other user"
                )

        transaction = transaction_crud.delete_transaction(self.db, transaction)
        return transaction

    def get_transactions(
        self,
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
        min_amount: int = None,
        max_amount: int = None,
    ):
        if RoleEnum.ADMIN not in self.logged_user.roles:
            user_id = self.logged_user.id

        if start_date and start_date != "":
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date and end_date != "":
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

        return transaction_crud.get_transactions(
            self.db,
            filter=filter,
            user_id=user_id,
            category_id=category_id,
            transaction_type=transaction_type,
            limit=limit,
            page=page,
            sort_by=sort_by,
            order=order,
            start_date=start_date,
            end_date=end_date,
            min_amount=min_amount,
            max_amount=max_amount,
        )
