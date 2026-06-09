from enum import Enum


class TransactionEnum(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


TransactionFilterEnum = Enum(
    "TransactionFilterEnum",
    {"ALL": "all", **{r.name: r.value for r in TransactionEnum}},
    type=str,
)
