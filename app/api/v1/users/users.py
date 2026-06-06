from fastapi import APIRouter

router = APIRouter(
    prefix="/users", tags=["Users"], responses={404: {"description": "Not Found"}}
)


@router.get("/me")
def get_current_user():
    return {"message": "Get current user"}


@router.put("/{id:int}")
def update_user(id: int):
    return {"message": f"Update user {id}"}


@router.delete("/{id:int}")
def delete_user(id: int):
    return {"message": f"Delete user {id}"}


@router.get("/{id:int}")
def get_user(id: int):
    return {"message": f"Get user {id}"}


@router.get("")
def get_users_list():
    return {"message": "Get users list"}
