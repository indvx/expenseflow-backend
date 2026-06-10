# Exit immediately if a command exits with a non-zero status
set -e

# 1. Run migrations to update the database to the latest version
echo "Running database migrations..."
alembic upgrade head

# 2. Start the FastAPI server using Uvicorn
echo "Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload
