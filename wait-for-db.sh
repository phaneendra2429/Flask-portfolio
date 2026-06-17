#!/bin/sh
# Waits until the PostgreSQL database is ready before starting the app.
# Usage: /wait-for-db.sh <command to run>

set -e

DB_HOST="${DB_HOST:-db}"
DB_PORT="${DB_PORT:-5432}"
MAX_RETRIES=30
RETRY_INTERVAL=2

echo "Waiting for PostgreSQL at $DB_HOST:$DB_PORT ..."

retries=0
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -q; do
  retries=$((retries + 1))
  if [ "$retries" -ge "$MAX_RETRIES" ]; then
    echo "ERROR: PostgreSQL did not become ready after $((MAX_RETRIES * RETRY_INTERVAL))s. Exiting."
    exit 1
  fi
  echo "  Attempt $retries/$MAX_RETRIES — not ready yet, retrying in ${RETRY_INTERVAL}s..."
  sleep "$RETRY_INTERVAL"
done

echo "PostgreSQL is ready. Starting application..."
exec "$@"
