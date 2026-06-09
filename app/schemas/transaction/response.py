from pydantic import BaseModel
from app.schemas.user.response import UserResponse
from app.schemas.category.response import CategoryResponse
import typing as t
from app.schemas.common_response import MetaDataResponse
from app.enums.transaction_enums import TransactionEnum


class TransactionResponse(BaseModel):
    id: int
    amount: float
    type: TransactionEnum
    transaction_date: t.Any
    description: t.Optional[str]
    category: CategoryResponse
    user: UserResponse
    created_at: t.Any
    updated_at: t.Any

    class ConfigDict:
        from_attributes = True


class TransactionsResponse(MetaDataResponse):
    transactions: t.List[TransactionResponse]

    class ConfigDict:
        from_attributes = True
