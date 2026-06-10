from fastapi import APIRouter, Depends
import typing as t
from app.schemas.report.response import (
    MonthlyReportResponse,
    YearlyReportResponse,
    DailyReportResponse,
    CategoryWiseExpenseResponse,
)
from app.db.dependencies import get_db
from app.core.security.auth import get_current_user
from app.sql.models.user import User
from sqlalchemy.orm import Session
from app.services.transaction.transaction import TransactionService

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
    responses={404: {"description": "Not Found"}},
)


@router.get("/yearly", response_model=t.List[YearlyReportResponse])
def get_yearly_report(
    year: t.Optional[int] = None,
    user_id: t.Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transaction_service = TransactionService(db, current_user)
    reports = transaction_service.get_report(
        report_type="yearly",
        year=year,
        user_id=user_id,
    )
    return reports


@router.get("/monthly", response_model=t.List[MonthlyReportResponse])
def get_monthly_report(
    year: t.Optional[int] = None,
    month: t.Optional[int] = None,
    user_id: t.Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transaction_service = TransactionService(db, current_user)
    reports = transaction_service.get_report(
        report_type="monthly",
        year=year,
        month=month,
        user_id=user_id,
    )
    return reports


@router.get("/daily", response_model=t.List[DailyReportResponse])
def get_monthly_report(
    year: t.Optional[int] = None,
    month: t.Optional[int] = None,
    day: t.Optional[int] = None,
    user_id: t.Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transaction_service = TransactionService(db, current_user)
    reports = transaction_service.get_report(
        report_type="daily",
        year=year,
        month=month,
        user_id=user_id,
        day=day,
    )
    return reports