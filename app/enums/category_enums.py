from enum import Enum


class CategoryType(Enum):
    INCOME = "income"
    EXPENSE = "expense"


CategoryFilterEnum = Enum(
    "CategoryFilterEnum",
    {"ALL": "all", **{r.name: r.value for r in CategoryType}},
    type=str,
)
