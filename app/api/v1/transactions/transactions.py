from fastapi import APIRouter, Depends
import typing as t
from app.schemas.transaction.request import (
    TransactionCreateRequest,
    TransactionUpdateRequest,
)
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.core.security.auth import get_current_user
from app.services.transaction.transaction import TransactionService
from app.schemas.transaction.response import TransactionResponse, TransactionsResponse
from app.enums.transaction_enums import TransactionFilterEnum

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
    responses={404: {"description": "Not Found"}},
)


@router.get("/", response_model=TransactionsResponse)
def get_transactions(
    filter: t.Optional[str] = None,
    page: t.Optional[int] = 1,
    sort_by: t.Optional[str] = "id",
    order: t.Literal["asc", "desc"] = "desc",
    limit: t.Optional[int] = 20,
    transaction_type: TransactionFilterEnum = TransactionFilterEnum.ALL,
    category_id: t.Optional[int] = None,
    start_date: t.Optional[str] = None,
    end_date: t.Optional[str] = None,
    min_amount: t.Optional[int] = None,
    max_amount: t.Optional[int] = None,
    user_id: t.Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: t.Any = Depends(get_current_user),
):
    transaction_service = TransactionService(db, current_user)
    transactions = transaction_service.get_transactions(
        filter=filter,
        page=page,
        sort_by=sort_by,
        order=order,
        limit=limit,
        transaction_type=transaction_type,
        category_id=category_id,
        start_date=start_date,
        end_date=end_date,
        min_amount=min_amount,
        max_amount=max_amount,
        user_id=user_id,
    )
    return transactions


@router.post("/", response_model=TransactionResponse)
def create_transaction(
    transaction: TransactionCreateRequest,
    db: Session = Depends(get_db),
    current_user: t.Any = Depends(get_current_user),
):
    transaction_service = TransactionService(db, current_user)
    new_transaction = transaction_service.create_transaction(transaction)
    return new_transaction


@router.get("/{id:int}", response_model=TransactionResponse)
def get_transaction(
    id: int,
    db: Session = Depends(get_db),
    current_user: t.Any = Depends(get_current_user),
):
    transaction_service = TransactionService(db, current_user)
    transaction = transaction_service.get_transaction(id)
    return transaction


@router.put("/{id:int}", response_model=TransactionResponse)
def update_transaction(
    id: int,
    transaction_data: TransactionUpdateRequest,
    db: Session = Depends(get_db),
    current_user: t.Any = Depends(get_current_user),
):
    transaction_service = TransactionService(db, current_user)
    updated_transaction = transaction_service.update_transaction(id, transaction_data)
    return updated_transaction


@router.delete("/{id:int}")
def delete_transaction(
    id: int,
    db: Session = Depends(get_db),
    current_user: t.Any = Depends(get_current_user),
):
    transaction_service = TransactionService(db, current_user)
    transaction_service.delete_transaction(id)
