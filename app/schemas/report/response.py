from pydantic import BaseModel, EmailStr
import typing as t


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr


class MonthlyReportResponse(BaseModel):
    year: int
    month: int
    total_income: float
    total_expense: float
    net_savings: float
    user: t.Optional[UserResponse] = None

    class ConfigDict:
        from_attributes = True


class YearlyReportResponse(BaseModel):
    year: int
    total_income: float
    total_expense: float
    net_savings: float
    user: t.Optional[UserResponse] = None

    class ConfigDict:
        from_attributes = True


class DailyReportResponse(BaseModel):
    year: int
    month: int
    day: int
    total_income: float
    total_expense: float
    net_savings: float
    user: t.Optional[UserResponse] = None

    class ConfigDict:
        from_attributes = True


class CategoryItemResponse(BaseModel):
    category_id: int
    category_name: str
    amount: float

    class ConfigDict:
        from_attributes = True


class CategoryWiseExpenseResponse(BaseModel):
    year: t.Optional[int] = None
    month: t.Optional[int] = None
    user: t.Optional[UserResponse] = None
    categories: t.List[CategoryItemResponse]

    class ConfigDict:
        from_attributes = True
