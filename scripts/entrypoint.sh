#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z web-db 6432; do
  sleep 0.1
done

echo "PostgreSQL started"

exec "$@"