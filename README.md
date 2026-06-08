# 💼 ExpenseFlow Backend API

**Professional Expense Management System** - A production-ready REST API for comprehensive expense tracking, budget management, and financial reporting.

---

## ✨ Overview

ExpenseFlow Backend is an enterprise-grade expense management API designed for businesses and individuals to efficiently track, categorize, and analyze their financial transactions. Built with modern technologies and best practices, it provides a robust foundation for expense management applications.

### Key Benefits
✅ **Real-time Financial Insights** - Comprehensive reporting and analytics  
✅ **Secure & Scalable** - JWT authentication with PostgreSQL backend  
✅ **Easy Integration** - RESTful API with comprehensive documentation  
✅ **Production Ready** - Docker support and database migrations  
✅ **Developer Friendly** - Interactive API documentation with Swagger UI  

---

## 🏗️ Architecture Overview

| Layer | Technology |
|-------|-----------|
| **API Framework** | FastAPI 0.136.3 |
| **Database** | PostgreSQL with SQLAlchemy 2.0.50 |
| **Authentication** | JWT (PyJWT 2.13.0) |
| **Migrations** | Alembic 1.18.4 |
| **Security** | Argon2 Password Hashing |
| **Containerization** | Docker & Docker Compose |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Docker & Docker Compose (optional)

### Installation

**1. Clone Repository**
```bash
git clone https://github.com/indvx/expenseflow-backend.git
cd expenseflow-backend
```

**2. Setup Environment**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**3. Configure Database**
```bash
cp .env copy .env
# Edit .env with your PostgreSQL credentials
```

**4. Initialize Database**
```bash
alembic upgrade head
```

**5. Start Server**
```bash
fastapi dev main.py
```

Server runs at: `http://localhost:8000`

---

## 📖 API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Core Modules

#### 🔐 **Authentication**
Secure user registration, login, and token management.

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `POST` | `/auth/register` | Create new user account |
| `POST` | `/auth/login` | Authenticate and receive tokens |
| `POST` | `/auth/refresh` | Refresh expired access token |
| `POST` | `/auth/logout` | Logout and invalidate tokens |

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secure_password"}'
```

---

#### 👥 **User Management**
Manage user profiles, permissions, and account settings.

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/users` | List all users with filtering |
| `GET` | `/users/me` | Get current user profile |
| `GET` | `/users/{id}` | Get specific user details |
| `PUT` | `/users/{id}` | Update user information |
| `DELETE` | `/users/{id}` | Delete user account |

**Query Parameters:**
```
search        - Search by name
page          - Page number (default: 1)
page_size     - Items per page (default: 20)
sort_by       - Sort field (name, created_at)
order         - asc or desc (default: asc)
status        - active, inactive
role          - admin, user, viewer
start_date    - YYYY-MM-DD
end_date      - YYYY-MM-DD
```

---

#### 📁 **Categories**
Organize expenses with flexible category management.

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/categories` | List categories |
| `POST` | `/categories` | Create new category |
| `GET` | `/categories/{id}` | Get category details |
| `PUT` | `/categories/{id}` | Update category |
| `DELETE` | `/categories/{id}` | Delete category |

**Query Parameters:**
```
search     - Filter by name
type       - expense, income, transfer
page       - Pagination
page_size  - Items per page
sort_by    - Sort field
order      - asc or desc
```

---

#### 💰 **Transactions**
Complete expense and income transaction management.

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/transactions` | List all transactions |
| `POST` | `/transactions` | Record new transaction |
| `GET` | `/transactions/{id}` | Get transaction details |
| `PUT` | `/transactions/{id}` | Update transaction |
| `DELETE` | `/transactions/{id}` | Delete transaction |

**Advanced Filtering:**
```
search       - Search by description
type         - expense, income
status       - completed, pending, rejected
category_id  - Filter by category
min_amount   - Minimum amount filter
max_amount   - Maximum amount filter
start_date   - Date range start (YYYY-MM-DD)
end_date     - Date range end (YYYY-MM-DD)
page         - Pagination
page_size    - Items per page
sort_by      - date, amount, category
order        - asc or desc
```

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/transactions?type=expense&min_amount=50&max_amount=500&start_date=2026-01-01" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

#### 📊 **Reports & Analytics**
Generate comprehensive financial insights and summaries.

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/reports/monthly` | Monthly expense summary |
| `GET` | `/reports/yearly` | Yearly financial overview |
| `GET` | `/reports/daily` | Daily transaction summary |
| `GET` | `/reports/category-summary` | Breakdown by category |

**Query Parameters:**
```
month   - Month number (1-12)
year    - Year (YYYY)
```

**Example Response:**
```json
{
  "period": "2026-06",
  "total_expense": 2450.50,
  "total_income": 5000.00,
  "net": 2549.50,
  "by_category": {
    "Groceries": 250.00,
    "Utilities": 150.00,
    "Entertainment": 200.50
  }
}
```

---

#### 🏥 **Health Check**
Monitor API availability and status.

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/health` | API health status |

---

## 🔐 Authentication & Security

### JWT Token Flow
```
1. User Login
   ↓
2. Receive: access_token (15min) + refresh_token (7 days)
   ↓
3. Use access_token in requests
   ↓
4. Before expiry, use refresh_token to get new tokens
```

### Authorization Header
```bash
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Security Features
- ✅ Argon2 password hashing
- ✅ JWT token-based authentication
- ✅ Token refresh mechanism
- ✅ Role-based access control
- ✅ HTTPS ready
- ✅ Database connection pooling

---

## 🐳 Docker Deployment

### Docker Setup
```bash
# Build image
docker build -t expenseflow-backend:latest .

# Run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Environment Configuration
Create `.env` file:
```env
DATABASE_URL=postgresql://user:password@db:5432/expenseflow
JWT_SECRET_KEY=your-super-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
DEBUG=False
```

---

## 💾 Database Management

### Schema Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "Add expense limits"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi[standard] | 0.136.3 | Web framework |
| SQLAlchemy | 2.0.50 | ORM & database toolkit |
| psycopg2-binary | 2.9.12 | PostgreSQL adapter |
| alembic | 1.18.4 | Database migrations |
| pwdlib[argon2] | 0.3.0 | Password hashing |
| pyjwt | 2.13.0 | JWT token handling |

---

## 📁 Project Structure

```
expenseflow-backend/
├── app/
│   ├── models/              # Database ORM models
│   ├── schemas/             # Pydantic validation schemas
│   ├── routes/              # API endpoints
│   ├── services/            # Business logic layer
│   ├── dependencies/        # FastAPI dependencies
│   └── config.py            # Configuration management
├── alembic/
│   ├── versions/            # Migration scripts
│   └── env.py               # Migration environment
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── alembic.ini             # Alembic settings
├── Dockerfile              # Container image definition
├── docker-compose.yml      # Multi-container setup
├── .env                    # Environment variables
└── README.md               # This file
```

---

## 🧪 Testing & Quality

```bash
# Run tests
pytest tests/ -v

# Coverage report
pytest --cov=app tests/

# Code formatting
black app/

# Linting
flake8 app/

# Type checking
mypy app/
```

---

## 📋 Response Format

### Success Response
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "amount": 150.50,
    "category": "Groceries",
    "date": "2026-06-08",
    "description": "Weekly shopping"
  },
  "message": "Transaction created successfully"
}
```

### Error Response
```json
{
  "status": "error",
  "code": "INVALID_REQUEST",
  "message": "Amount must be greater than 0",
  "details": {
    "field": "amount",
    "error": "validation_error"
  }
}
```

---

## 🔗 Integration Examples

### JavaScript/Node.js
```javascript
const response = await fetch('http://localhost:8000/api/v1/transactions', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  }
});
const data = await response.json();
```

### Python
```python
import requests

headers = {'Authorization': f'Bearer {access_token}'}
response = requests.get(
  'http://localhost:8000/api/v1/transactions',
  headers=headers
)
transactions = response.json()
```

### cURL
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:8000/api/v1/transactions
```

---

## 🛠️ Configuration

### Environment Variables
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/expenseflow

# JWT
JWT_SECRET_KEY=your-secret-key-min-32-chars
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Server
DEBUG=False
API_TITLE=ExpenseFlow API
API_VERSION=1.0.0

# CORS
ALLOWED_ORIGINS=http://localhost:3000,https://app.expenseflow.com
```

---

## 📊 Performance & Scalability

- ✅ Database connection pooling
- ✅ Request pagination (configurable page size)
- ✅ Indexed database queries
- ✅ Efficient ORM with lazy loading
- ✅ Redis caching ready
- ✅ Load balancer compatible
- ✅ Horizontal scalability with Docker

---

## 🐛 Troubleshooting

### Database Connection Error
```bash
# Check PostgreSQL is running
psql -U postgres

# Verify DATABASE_URL in .env
echo $DATABASE_URL
```

### JWT Token Invalid
```bash
# Ensure JWT_SECRET_KEY is set in .env
# Tokens expire after ACCESS_TOKEN_EXPIRE_MINUTES
# Use /auth/refresh endpoint to get new token
```

### Port Already in Use
```bash
# Change port or kill process
lsof -i :8000
kill -9 <PID>
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** changes (`git commit -m 'Add amazing feature'`)
4. **Push** to branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add tests for new features
- Update documentation
- Use meaningful commit messages

---

## 📝 License

MIT License © 2026 ExpenseFlow. See [LICENSE](LICENSE) file for details.

---

## 💬 Support & Feedback

**Have questions or found an issue?**

- 📧 **Email**: support@expenseflow.com
- 🐛 **GitHub Issues**: [Report Bug](https://github.com/indvx/expenseflow-backend/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/indvx/expenseflow-backend/discussions)
- 📚 **Documentation**: [Full Docs](https://docs.expenseflow.com)

---

## 🙌 Acknowledgments

Built with FastAPI, SQLAlchemy, and PostgreSQL - the modern Python stack for building scalable APIs.

---

**ExpenseFlow Backend** - Simplifying Expense Management  
*Last Updated: June 2026*

**[⬆ back to top](#-expenseflow-backend-api)**
