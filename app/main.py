from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html
from app.api.v1.routers import router as api_router
from app.core.exceptions.exceptions import AppException
from app.core.exceptions.exception_handlers import app_exception_handler
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="ExpenseFlow API",
    description="ExpenseFlow is a personal finance management application that helps you track your income and expenses, set budgets, and achieve your financial goals.",
    version="1.0.0",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    debug=os.getenv("DEBUG", False),
    docs_url=None,
)


app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/docs", include_in_schema=False)
async def swagger_ui_html(req: Request) -> HTMLResponse:
    root_path = req.scope.get("root_path", "").rstrip("/")
    openapi_url = root_path + app.openapi_url
    oauth2_redirect_url = app.swagger_ui_oauth2_redirect_url
    if oauth2_redirect_url:
        oauth2_redirect_url = root_path + oauth2_redirect_url
    return get_swagger_ui_html(
        openapi_url=openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=oauth2_redirect_url,
        init_oauth=app.swagger_ui_init_oauth,
        swagger_favicon_url=f"{root_path}/static/expenseflow.svg",
        swagger_ui_parameters=app.swagger_ui_parameters,
    )


app.add_exception_handler(
    AppException,
    app_exception_handler,
)
app.include_router(api_router)


@app.get("/")
def root():
    return {"message": "Welcome to ExpenseFlow API"}
