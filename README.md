BASE URL:
http://localhost:8000/api/v1

## AUTH MODULE

POST /auth/register
POST /auth/login
POST /auth/refresh
POST /auth/logout

## USERS MODULE

GET /users?search=john&page=1&page_size=20&sort_by=name&order=asc&limit=100&status=active&role=admin&start_date=YYYY-MM-DD&end_date=YYYY-MM-DD&
GET /users/me
GET /users/{id}
PUT /users/{id}
DELETE /users/{id}

## CATEGORIES MODULE

GET /categories?search=groceries&page=1&page_size=20&sort_by=name&order=asc&limit=100&type=expense&start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
POST /categories
GET /categories/{id}
PUT /categories/{id}
DELETE /categories/{id}

## TRANSACTIONS MODULE

GET /transactions?search=salary&page=1&page_size=20&sort_by=date&order=desc&limit=100&status=completed&type=expense&category_id=1&start_date=YYYY-MM-DD&end_date=YYYY-MM-DD&min_amount=100&max_amount=5000&user_id=1
POST /transactions
GET /transactions/{id}
PUT /transactions/{id}
DELETE /transactions/{id}

## REPORTS MODULE (NO DATABASE TABLE)

GET /reports/monthly?month=6&year=2026
GET /reports/yearly?year=2026
GET /reports/category-summary?month=6&year=2026
GET /reports/daily?month=6&year=2026

## HEALTH MODULE

GET /health
