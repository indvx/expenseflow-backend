from fastapi import APIRouter
import typing as t

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
    responses={404: {"description": "Not Found"}},
)


@router.get("/{report_type}")
def get_report(
    report_type: t.Literal["monthly", "yearly", "category-summary", "daily"],
    year: t.Optional[int] = None,
    month: t.Optional[int] = None,
    user_id: t.Optional[int] = None,
):
    return {"message": f"Get {report_type} report {month} {year}"}
