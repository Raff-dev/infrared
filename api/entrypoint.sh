#!/bin/sh

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    echo "Waiting for postgres..."
    sleep 0.1
done

echo "PostgreSQL started"

echo "Collect static files"
python manage.py collectstatic --noinput

echo "Applying migrations"
python manage.py migrate

echo "Starting server"
gunicorn --bind 0.0.0.0:8000 api.wsgi
