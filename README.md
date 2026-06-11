# 💼 ExpenseFlow Backend API

**Professional Expense Management System** - A production-ready REST API for comprehensive expense tracking, budget management, and financial reporting. Built with FastAPI, PostgreSQL, and Docker for seamless containerized deployment.

---

## ✨ Overview

ExpenseFlow Backend is an enterprise-grade expense management API designed for businesses and individuals to efficiently track, categorize, and analyze their financial transactions. Built with modern Python technologies and fully containerized with Docker for production deployment.

### Key Benefits
✅ **Real-time Financial Insights** - Comprehensive reporting and analytics  
✅ **Secure & Scalable** - JWT authentication with PostgreSQL backend  
✅ **Easy Integration** - RESTful API with comprehensive documentation  
✅ **Production Ready** - Docker support and database migrations  
✅ **Developer Friendly** - Interactive API documentation with Swagger UI  
✅ **Containerized** - Multi-stage Docker builds with Docker Compose  

---

## 🏗️ Architecture Overview

| Component | Technology | Version |
|-----------|-----------|---------|
| **API Framework** | FastAPI | 0.136.3 |
| **Database** | PostgreSQL | 16-alpine |
| **ORM & Toolkit** | SQLAlchemy | 2.0.50 |
| **Authentication** | JWT (PyJWT) | 2.13.0 |
| **Password Hashing** | Argon2 | pwdlib 0.3.0 |
| **Migrations** | Alembic | 1.18.4 |
| **ASGI Server** | Uvicorn | Latest |
| **Containerization** | Docker & Compose | Latest |
| **Python Version** | Python | 3.11-slim |

### Project Structure

```
expenseflow-backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth/              # Authentication endpoints
│   │       ├── categories/        # Category management
│   │       ├── transactions/      # Transaction handling
│   │       ├── users/             # User management
│   │       ├── reports/           # Analytics & reporting
│   │       └── routers.py         # Route aggregation
│   ├── core/
│   │   ├── exceptions/            # Custom exceptions & handlers
│   │   └── security/              # Authentication & security
│   ├── services/
│   │   ├── auth/                  # Auth business logic
│   │   ├── users/                 # User service
│   │   ├── category/              # Category service
│   │   ├── transaction/           # Transaction service
│   │   └── comman.py              # Shared utilities
│   ├── db/
│   │   ├── dependencies.py        # DB session management
│   │   └── models.py              # SQLAlchemy models
│   ├── schemas/                   # Pydantic models for validation
│   ├── sql/
│   │   └── cruds.py               # Database CRUD operations
│   ├── enums/                     # Application enumerations
│   ├── static/                    # Static assets
│   ├── templates/                 # HTML templates
│   └── main.py                    # Application entry point
├── alembic/
│   ├── versions/                  # Migration scripts
│   ├── env.py                     # Migration environment config
│   └── script.py.mako             # Migration template
├── Dockerfile                     # Multi-stage Docker build
├── docker-compose.yml             # Docker Compose orchestration
├── .dockerignore                  # Docker build optimization
├── requirements.txt               # Python dependencies
├── alembic.ini                    # Alembic configuration
├── .env.example                   # Environment template
└── README.md                      # This file
```

---

## 🚀 Quick Start

### Prerequisites
- **Docker & Docker Compose** (Recommended) - For containerized setup
- **Python 3.11+** - For local development
- **PostgreSQL 12+** - For standalone setup
- **pip** - Python package manager

### Option 1: Docker Compose (Recommended) ⭐

This is the quickest and most reliable way to run the API container. Note that the `docker-compose.yml` is configured to run the `api` service and connect to a PostgreSQL database on the host machine or external server via `host.docker.internal` (or custom host).

**1. Clone Repository**
```bash
git clone https://github.com/indvx/expenseflow-backend.git
cd expenseflow-backend
```

**2. Create Environment File**
```bash
cp ".env copy" .env
```

**3. Edit `.env` with Your Configuration**
Ensure that `DB_HOST` is set correctly (e.g., `host.docker.internal` to connect to PostgreSQL running on your host machine) and set other database details.
```env
# Database Configuration
DB_CONNECTION=postgresql+psycopg2
DB_HOST=host.docker.internal
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_NAME=expenseflow-db

# JWT Configuration
SECRET_KEY=your-super-secret-key-min-32-chars-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Server Configuration
DEBUG=False
PORT=8001
```

**4. Start Services**
You can use the helper shell scripts or run `docker compose` directly:
```bash
# Start the API service in the background (runs migrations on startup)
./up.sh

# Or run using docker compose directly
docker compose up -d

# View logs
docker compose logs -f api

# Check service status
docker compose ps
```

**5. Access the API**
- API Base URL: `http://localhost:8003`
- Swagger UI: `http://localhost:8003/docs`
- ReDoc: `http://localhost:8003/redoc`
- Health Check: `http://localhost:8003/health`

### Option 2: Docker Build Only

If you want to build the image separately:

```bash
# Build image
docker build -t expenseflow-backend:latest .

# Run container with external PostgreSQL
docker run -p 8003:8003 \
  --env-file .env \
  expenseflow-backend:latest
```

### Option 3: Local Development Setup

**1. Create Virtual Environment**
```bash
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

**2. Install Dependencies**
```bash
pip install -r requirements.txt
```

**3. Setup Database**
```bash
# Ensure PostgreSQL is running on localhost:5432
# Create .env file (see Option 1 step 3)

# Run migrations
alembic upgrade head
```

**4. Start Server**
```bash
# Option A: Using uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload

# Option B: Using FastAPI CLI
fastapi dev app/main.py

# Option C: Using start script (if available)
chmod +x start.sh
./start.sh
```

Server runs at: `http://localhost:8003`

---

## 🐳 Docker Setup Details

### Docker Architecture

Our Docker setup uses a **multi-stage build** for optimal production images:

1. **Builder Stage** - Installs build dependencies and compiles Python packages
2. **Runtime Stage** - Contains only runtime dependencies, reducing image size by ~60%

### Benefits of Our Docker Setup

✅ **Optimized Image Size** - Multi-stage builds reduce image from 1.2GB to ~400MB  
✅ **Security** - Non-root user execution (appuser:1000)  
✅ **Health Checks** - Automatic container health monitoring  
✅ **Environment Variables** - Flexible configuration via .env  
✅ **Volume Persistence** - Database data persists across container restarts  
✅ **Auto-Migration** - Database migrations run automatically on startup  

### Docker Compose Services

**FastAPI Service** (`api`)
- Builds from: `./Dockerfile`
- Port: `8001` (exposed dynamically or mapped via environment)
- Health Check: Every 30 seconds
- Auto-restart: Unless stopped
- Volumes: Bind mount to local codebase for development/hot-reloading
- Command: Starts `uvicorn` and hot-reloads on source changes. (Note: Database migrations run automatically via `entrypoint.sh` when `uvicorn` starts)

### Environment Variables

```env
# Database Configuration
DB_CONNECTION=postgresql+psycopg2  # SQL database driver connection
DB_HOST=host.docker.internal       # Use host.docker.internal to connect to host DB
DB_PORT=5432                       # Database port
DB_USER=postgres                   # Database user
DB_PASSWORD=secure_password        # Database password
DB_NAME=expenseflow-db             # Database name

# JWT Authentication
SECRET_KEY=your-secret-key         # Min 32 chars, use strong random value
ALGORITHM=HS256                    # JWT algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=30     # Token lifetime
REFRESH_TOKEN_EXPIRE_DAYS=7        # Refresh token lifetime

# Server Configuration
DEBUG=False                        # Enable debugging mode (never in production)
```

### Docker Commands Reference

```bash
# Start service in background (using helper script)
./up.sh

# Stop service (using helper script)
./down.sh

# Restart service (using helper script)
./restart.sh

# Start using docker compose
docker compose up -d

# Stop using docker compose
docker compose down

# View API logs
docker compose logs -f api

# Check service status
docker compose ps

# Execute bash command inside the running API container
docker compose exec api bash

# Rebuild image without cache
docker compose build --no-cache
```

---

## 📖 API Documentation

### Base URL
```
http://localhost:8003/api/v1
```

### Interactive Documentation
- **Swagger UI**: `http://localhost:8003/docs`
- **ReDoc**: `http://localhost:8003/redoc`
- **Welcome**: `http://localhost:8003/`
- **Health Check**: `http://localhost:8003/health`

### Core Modules

#### 🔐 **Authentication** (`/auth`)
Secure user registration, login, and token management.

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `POST` | `/auth/register` | Create new user account |
| `POST` | `/auth/login` | Authenticate and receive tokens |
| `POST` | `/auth/refresh` | Refresh expired access token |
| `POST` | `/auth/logout` | Logout and invalidate tokens |

**Example Register Request:**
```bash
curl -X POST "http://localhost:8003/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePassword123!",
    "confirm_password": "SecurePassword123!"
  }'
```

**Example Login Request:**
```bash
curl -X POST "http://localhost:8003/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePassword123!"
  }'
```

---

#### 👥 **User Management** (`/users`)
Manage user profiles, permissions, and account settings.

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/users` | List all users with filtering |
| `POST` | `/users/add` | Invite a new user (Admin only, sends email invite) |
| `GET` | `/users/me` | Get current user profile |
| `GET` | `/users/{id}` | Get specific user details |
| `PUT` | `/users/{id}` | Update user information |
| `DELETE` | `/users/{id}` | Delete user account |
| `POST` | `/users/reset-password-request` | Request password reset (sends temporary password) |

**Query Parameters (for GET /users):**
```
filter        - Search by username or email
user_id       - Filter by specific user ID
status        - all, active, inactive (default: all)
limit         - Items per page (default: 10)
page          - Page number (default: 1)
role          - all, admin, user, guest (default: all)
sort_by       - Sort field (id, username, email, created_at) (default: id)
order         - asc or desc (default: desc)
start_date    - Start date filter (YYYY-MM-DD)
end_date      - End date filter (YYYY-MM-DD)
```

---

#### 📁 **Categories** (`/categories`)
Organize expenses with flexible category management.

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/categories` | List categories |
| `POST` | `/categories` | Create new category |
| `GET` | `/categories/{id}` | Get category details |
| `PUT` | `/categories/{id}` | Update category |
| `DELETE` | `/categories/{id}` | Delete category |

---

#### 💰 **Transactions** (`/transactions`)
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

**Example Transaction Request:**
```bash
curl -X POST "http://localhost:8003/api/v1/transactions" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 150.50,
    "category_id": 1,
    "description": "Weekly groceries",
    "type": "expense"
  }'
```

---

#### 📊 **Reports & Analytics** (`/reports`)
Generate comprehensive financial insights and summaries.

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/reports/yearly` | Yearly financial overview |
| `GET` | `/reports/monthly` | Monthly expense summary |
| `GET` | `/reports/daily` | Daily transaction summary |

**Example Response (Yearly/Monthly/Daily list):**
```json
[
  {
    "year": 2026,
    "month": 6,
    "day": 0,
    "total_income": 5000.0,
    "total_expense": 2450.5,
    "net_savings": 2549.5,
    "user": {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com"
    }
  }
]
```

---

## 🔐 Authentication & Security

### JWT Token Flow
```
1. User Registration/Login
   ↓
2. Receive: access_token + refresh_token
   ↓
3. Use access_token in Authorization header
   ↓
4. Before expiry, use refresh_token to get new access_token
```

### Authorization Header
```bash
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Security Features
- ✅ **Argon2 Password Hashing** - Military-grade password security
- ✅ **JWT Token Authentication** - Stateless, scalable auth
- ✅ **Token Refresh Mechanism** - Automatic token rotation
- ✅ **Role-Based Access Control** - Granular permission management
- ✅ **HTTPS Ready** - Easy reverse proxy setup
- ✅ **Database Connection Pooling** - Optimized DB access
- ✅ **Exception Handling** - Secure error responses
- ✅ **Non-root Docker User** - Container security best practice

### Security Best Practices

1. **Change SECRET_KEY in Production**
   ```env
   SECRET_KEY=generate-a-strong-32-char-random-string
   ```

2. **Use Strong Database Password**
   ```env
   DB_PASSWORD=GenerateStrongPassword123!@#
   ```

3. **Enable HTTPS**
   - Use a reverse proxy (Nginx, Caddy)
   - Let's Encrypt SSL certificates

4. **Environment-Specific Config**
   - Use different `.env` files for dev/staging/production
   - Never commit `.env` to version control

---

## 💾 Database Management

### Running Migrations

```bash
# Apply all pending migrations
alembic upgrade head

# Apply specific number of migrations
alembic upgrade +2

# Create new migration (auto-generate from model changes)
alembic revision --autogenerate -m "Add expense limits"

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

### With Docker Compose

Migrations run **automatically** on container startup through `entrypoint.sh` when launching the FastAPI `uvicorn` server. There is no need to manually trigger them when starting with `docker compose` or scripts.

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi[standard] | 0.136.3 | Web framework with built-in extras |
| SQLAlchemy | 2.0.50 | ORM & database toolkit |
| psycopg2-binary | 2.9.12 | PostgreSQL adapter |
| alembic | 1.18.4 | Database migrations |
| pwdlib[argon2] | 0.3.0 | Argon2 password hashing |
| pyjwt | 2.13.0 | JWT token handling |
| uvicorn | Latest | ASGI server |
| python-dotenv | Latest | Environment variables |

---

## 📋 Response Format

### Success Response
Endpoints directly return the serialized Pydantic model representation. For example, a transaction creation request returns:
```json
{
  "id": 1,
  "amount": 150.50,
  "type": "expense",
  "transaction_date": "2026-06-11",
  "description": "Weekly groceries",
  "category": {
    "id": 1,
    "name": "Groceries",
    "user": {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com"
    },
    "created_at": "2026-06-11T12:00:00",
    "updated_at": "2026-06-11T12:00:00"
  },
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  },
  "created_at": "2026-06-11T12:00:00",
  "updated_at": "2026-06-11T12:00:00"
}
```

### Error Response
API errors managed by custom application exceptions return a structured error format:
```json
{
  "success": false,
  "message": "Error details/message explaining the failure"
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

### Environment Variables Reference

```env
# ============= Database Configuration =============
DB_CONNECTION=postgresql+psycopg2  # Database connection driver
DB_HOST=host.docker.internal       # Database host
DB_PORT=5432                       # PostgreSQL port
DB_USER=postgres                   # Database user
DB_PASSWORD=password               # Database password
DB_NAME=expenseflow-db             # Database name

# ============= JWT Configuration =============
SECRET_KEY=your-secret-key-min-32-chars  # Secret key for signing tokens
ALGORITHM=HS256                          # Token algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=30           # Access token lifetime
REFRESH_TOKEN_EXPIRE_DAYS=7              # Refresh token lifetime

# ============= Server Configuration =============
DEBUG=False                # Debug mode
PORT=8001                  # Application port
APP_DOMAIN=http://localhost:8003  # App domain URL for emails

# ============= Optional: SMTP/Email Configuration =============
SMTP_HOST=172.19.0.4       # SMTP server host
SMTP_PORT=1025             # SMTP server port
SMTP_SENDER=noreply@expenseflow.local
SMTP_USERNAME=             # SMTP username (optional)
SMTP_PASSWORD=             # SMTP password (optional)
```

---

## 📊 Performance & Scalability

- ✅ **Database Connection Pooling** - Optimized DB access
- ✅ **Request Pagination** - Configurable page size
- ✅ **Indexed Database Queries** - Fast lookups
- ✅ **Efficient ORM** - SQLAlchemy with lazy loading
- ✅ **Redis Caching Ready** - For session/data caching
- ✅ **Load Balancer Compatible** - Horizontal scaling
- ✅ **Docker Horizontal Scaling** - Multiple container instances
- ✅ **Exception Handling** - Graceful error responses

---

## 🐛 Troubleshooting

### Docker Compose Issues

**Cannot connect to database**
```bash
# Check if database is healthy
docker-compose ps

# View database logs
docker-compose logs db

# Ensure .env has correct credentials
docker-compose exec api cat /app/.env
```

**Port already in use**
```bash
# Change port in docker-compose.yml or .env
API_PORT=8004
DB_PORT=5433

# Or kill existing process
lsof -i :8003
kill -9 <PID>
```

**Container won't start**
```bash
# View logs with verbose output
docker-compose logs --follow api

# Rebuild without cache
docker-compose build --no-cache api
docker-compose up api
```

### Database Connection Error

```bash
# Check PostgreSQL is running
docker-compose ps db

# Verify DATABASE_URL in .env
echo $DB_HOST
echo $DB_PORT
echo $DB_USER

# Test connection
docker-compose exec db psql -U postgres -d expenseflow
```

### JWT Token Invalid

```bash
# Ensure SECRET_KEY is set in .env
# Tokens expire after ACCESS_TOKEN_EXPIRE_MINUTES
# Use /auth/refresh endpoint to get new token
```

### Migration Issues

```bash
# Check current migration status
docker-compose exec api alembic current

# View all migrations
docker-compose exec api alembic history

# If migrations are out of sync
docker-compose exec api alembic downgrade base
docker-compose exec api alembic upgrade head
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
- Ensure Docker builds work: `docker-compose build`

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

Built with **FastAPI**, **SQLAlchemy**, **PostgreSQL**, and **Docker** - the modern Python stack for building scalable, containerized APIs.

Special thanks to the open-source community for the excellent tools and libraries.

---

**ExpenseFlow Backend** - Simplifying Expense Management  
*Last Updated: June 2026*

**[⬆ back to top](#-expenseflow-backend-api)**
