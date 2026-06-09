from pydantic import BaseModel
import typing as t
from app.enums.transaction_enums import TransactionEnum


class TransactionCreateRequest(BaseModel):
    amount: float
    description: str
    type: TransactionEnum = TransactionEnum.EXPENSE
    category_id: int
    user_id: t.Optional[int] = None


class TransactionUpdateRequest(BaseModel):
    amount: t.Optional[float] = None
    description: t.Optional[str] = None
    type: t.Optional[TransactionEnum] = TransactionEnum.EXPENSE
    category_id: t.Optional[int] = None
    user_id: t.Optional[int] = None
