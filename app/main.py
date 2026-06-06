from fastapi import FastAPI
from app.api.v1.routers import router as api_router

app = FastAPI(
    title="ExpenseFlow API",
    description="ExpenseFlow is a personal finance management application that helps you track your income and expenses, set budgets, and achieve your financial goals.",
    version="1.0.0",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

app.include_router(api_router)


@app.get("/")
def root():
    return {"message": "Welcome to ExpenseFlow API"}
