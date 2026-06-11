#!/bin/sh
set -ex

echo "Arguments: $@"

if [ "$1" = "uvicorn" ]; then
  echo "Running database migrations..."
  alembic upgrade head
  echo "Migration finished"
fi

echo "Starting application"
exec "$@"