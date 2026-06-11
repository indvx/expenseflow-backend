# Exit immediately if a command exits with a non-zero status
set -e
docker compose down && docker compose up -d 