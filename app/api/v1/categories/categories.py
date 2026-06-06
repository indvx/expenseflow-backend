from fastapi import APIRouter
import typing as t

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
    responses={404: {"description": "Not Found"}},
)


@router.get("")
def get_categories(
    search: t.Optional[str] = None,
    sort_by: t.Optional[str] = None,
    order: t.Literal["asc", "desc"] = "asc",
    type: t.Literal["income", "expense"] = "all",
    page: t.Optional[int] = 1,
    limit: t.Optional[int] = 20,
    start_date: t.Optional[str] = None,
    end_date: t.Optional[str] = None,
):
    return {"message": "Get categories"}


@router.post("")
def create_category():
    return {"message": "Create category"}


@router.get("/{id:int}")
def get_category(id: int):
    return {"message": f"Get category {id}"}


@router.put("/{id:int}")
def update_category(id: int):
    return {"message": f"Update category {id}"}


@router.delete("/{id:int}")
def delete_category(id: int):
    return {"message": f"Delete category {id}"}
