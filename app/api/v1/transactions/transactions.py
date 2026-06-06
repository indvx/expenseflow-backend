from fastapi import APIRouter, HTTPException
import typing as t

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
    responses={404: {"description": "Not Found"}},
)


@router.get("/")
def get_transactions(
    search: t.Optional[str] = None,
    page: t.Optional[int] = 1,
    sort_by: t.Optional[str] = None,
    order: t.Literal["asc", "desc"] = "desc",
    limit: t.Optional[int] = 20,
    status: t.Literal["all", "pending", "completed", "cancelled"] = "all",
    type: t.Literal["all", "income", "expense"] = "all",
    category_id: t.Optional[int] = None,
    start_date: t.Optional[str] = None,
    end_date: t.Optional[str] = None,
    min_amount: t.Optional[int] = None,
    max_amount: t.Optional[int] = None,
    user_id: t.Optional[int] = None,
):
    return {"message": "Get transactions"}


@router.post("/")
def create_transaction():
    return {"message": "Create transaction"}


@router.get("/{id:int}")
def get_transaction(id: int):
    return {"message": f"Get transaction {id}"}


@router.put("/{id:int}")
def update_transaction(id: int):
    return {"message": f"Update transaction {id}"}


@router.delete("/{id:int}")
def delete_transaction(id: int):
    return {"message": f"Delete transaction {id}"}
