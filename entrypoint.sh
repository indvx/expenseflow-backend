#!/bin/sh
# Exit immediately if a command exits with a non-zero status
set -e

# Only run migrations when starting the FastAPI server
if [ "$1" = "uvicorn" ]; then
  echo "Running database migrations..."
  alembic upgrade head
fi

# Execute the CMD instruction
exec "$@"
