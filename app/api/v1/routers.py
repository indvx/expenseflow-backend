from fastapi import APIRouter
from app.api.v1.auth import auth
from app.api.v1.users import users
from app.api.v1.categories import categories
from app.api.v1.transactions import transactions
from app.api.v1.reports import reports


router = APIRouter(prefix="/api/v1")

router.include_router(auth.router)
router.include_router(users.router)
router.include_router(categories.router)
router.include_router(transactions.router)
router.include_router(reports.router)
