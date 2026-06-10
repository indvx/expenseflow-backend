# 💼 ExpenseFlow Backend API

**Professional Expense Management System** - A production-ready REST API for comprehensive expense tracking, budget management, and financial reporting.

---

## ✨ Overview

ExpenseFlow Backend is an enterprise-grade expense management API designed for businesses and individuals to efficiently track, categorize, and analyze their financial transactions. Built with modern FastAPI framework and PostgreSQL database.

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
| **ASGI Server** | Uvicorn |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Docker & Docker Compose (optional)
- pip (Python package manager)

### Installation

**1. Clone Repository**
```bash
git clone https://github.com/indvx/expenseflow-backend.git
cd expenseflow-backend
```

**2. Setup Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**3. Configure Database**
```bash
# Copy environment template
cp ".env copy" .env

# Edit .env with your PostgreSQL credentials
# Example:
# DB_HOST=localhost
# DB_PORT=5432
# DB_USER=postgres
# DB_PASSWORD=your_password
# DB_NAME=expenseflow
```

**4. Initialize Database**
```bash
alembic upgrade head
```

**5. Start Server**
```bash
# Option 1: Using uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload

# Option 2: Using the provided start script
chmod +x start.sh
./start.sh

# Option 3: Using FastAPI dev command
fastapi dev app/main.py
```

Server runs at: `http://localhost:8003` (or `http://localhost:8000` if using fastapi dev)

API Documentation available at: `http://localhost:8003/docs`

---

## 📖 API Documentation

### Base URL
```
http://localhost:8003/api/v1
```

### Interactive Documentation
- **Swagger UI**: http://localhost:8003/docs
- **ReDoc**: http://localhost:8003/redoc
- **Root Endpoint**: http://localhost:8003/ (Welcome message)
- **Health Check**: http://localhost:8003/health

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
curl -X POST "http://localhost:8003/api/v1/auth/login" \
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
curl -X GET "http://localhost:8003/api/v1/transactions?type=expense&min_amount=50&max_amount=500&start_date=2026-01-01" \
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
2. Receive: access_token + refresh_token
   ↓
3. Use access_token in requests
   ↓
4. Before expiry, use refresh_token to get new token
```

### Token Configuration (from .env)
```
ACCESS_TOKEN_EXPIRE_MINUTES = 15   # Default token lifetime
REFRESH_TOKEN_EXPIRE_DAYS = 7      # Refresh token lifetime
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
- ✅ Exception handling with custom error responses

---

## 🐳 Docker Deployment

### Docker Setup
```bash
# Build image
docker build -t expenseflow-backend:latest .

# Run container
docker run -p 8003:8003 --env-file .env expenseflow-backend:latest

# Stop container
docker stop <container_id>
```

### Using Docker Compose (if docker-compose.yml exists)
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Environment Configuration
Create `.env` file from template:
```env
# Database Configuration
DB_CONNECTION=postgresql
DB_HOST=db
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_NAME=expenseflow

# JWT Authentication
SECRET_KEY=your-super-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Server Configuration
DEBUG=False
API_TITLE=ExpenseFlow API
API_VERSION=1.0.0
```

---

## 💾 Database Management

### Schema Migrations
```bash
# Create new migration (auto-generate from model changes)
alembic revision --autogenerate -m "Add expense limits"

# Apply all pending migrations
alembic upgrade head

# Apply specific number of migrations
alembic upgrade +2

# Rollback one migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision_id>

# View migration history
alembic history

# View current revision
alembic current
```

### Database Connection URL Format
```
postgresql://user:password@host:port/database
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
| uvicorn | Latest | ASGI server |
| python-dotenv | Latest | Environment variables |

---

## 📁 Project Structure

```
expenseflow-backend/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── routers/          # API endpoint handlers
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── core/
│   │   ├── exceptions/           # Custom exception handlers
│   │   │   ├── exceptions.py
│   │   │   ├── exception_handlers.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── models/                   # SQLAlchemy ORM models
│   ├── schemas/                  # Pydantic validation schemas
│   ├── services/                 # Business logic layer
│   ├── dependencies/             # FastAPI dependencies (DB, Auth, etc.)
│   ├── config.py                 # Configuration management
│   └── main.py                   # Application entry point (in app/ folder)
├── alembic/
│   ├── versions/                 # Database migration scripts
│   ├── env.py                    # Migration environment configuration
│   └── script.py.mako            # Migration script template
├── main.py                       # Application entry point (alternative location)
├── start.sh                      # Startup script with migrations
├── requirements.txt              # Python dependencies
├── alembic.ini                   # Alembic configuration
├── ".env copy"                   # Environment variables template
├── .env                          # Environment variables (git-ignored)
├── .gitignore                    # Git ignore rules
├── Dockerfile                    # Container image definition
├── docker-compose.yml            # Multi-container setup (if present)
└── README.md                     # This file
```

---

## 🧪 Testing & Quality

```bash
# Run tests (if test suite exists)
pytest tests/ -v

# Coverage report
pytest --cov=app tests/

# Code formatting
black app/

# Linting
flake8 app/

# Type checking
mypy app/

# Sort imports
isort app/
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
const response = await fetch('http://localhost:8003/api/v1/transactions', {
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
  'http://localhost:8003/api/v1/transactions',
  headers=headers
)
transactions = response.json()
```

### cURL
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:8003/api/v1/transactions
```

---

## 🛠️ Configuration

### Environment Variables
```env
# Database
DB_CONNECTION=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=expenseflow

# JWT
SECRET_KEY=your-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Server
DEBUG=False
API_TITLE=ExpenseFlow API
API_VERSION=1.0.0

# CORS (if configured)
ALLOWED_ORIGINS=http://localhost:3000,https://app.expenseflow.com
```

### Server Port Configuration
- **Default Port**: 8003 (see `start.sh`)
- **FastAPI dev**: 8000 (when using `fastapi dev`)
- **Custom**: Pass `--port` flag to uvicorn

---

## 📊 Performance & Scalability

- ✅ Database connection pooling
- ✅ Request pagination (configurable page size)
- ✅ Indexed database queries
- ✅ Efficient ORM with lazy loading
- ✅ Redis caching ready
- ✅ Load balancer compatible
- ✅ Horizontal scalability with Docker
- ✅ Exception handling for graceful error responses

---

## 🐛 Troubleshooting

### Database Connection Error
```bash
# Check PostgreSQL is running
psql -U postgres

# Verify DATABASE_URL in .env
echo $DB_HOST
echo $DB_PORT
echo $DB_USER
```

### JWT Token Invalid
```bash
# Ensure SECRET_KEY is set in .env
# Tokens expire after ACCESS_TOKEN_EXPIRE_MINUTES
# Use /auth/refresh endpoint to get new token
```

### Port Already in Use
```bash
# Check what's using port 8003
lsof -i :8003

# Kill process using the port
kill -9 <PID>

# Or run on different port
uvicorn app.main:app --port 8004
```

### Migration Issues
```bash
# Check current migration status
alembic current

# View all migrations
alembic history

# If migrations are out of sync, downgrade and upgrade
alembic downgrade base  # Revert all
alembic upgrade head    # Reapply all
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
- Test your changes before submitting PR

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

Built with FastAPI, SQLAlchemy, PostgreSQL, and Uvicorn - the modern Python stack for building scalable APIs.

Special thanks to the open-source community for the excellent tools and libraries.

---

**ExpenseFlow Backend** - Simplifying Expense Management  
*Last Updated: June 2026*

**[⬆ back to top](#-expenseflow-backend-api)**
