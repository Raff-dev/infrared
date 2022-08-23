#!/bin/sh

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    echo "Waiting for postgres..."
    sleep 0.1
done

echo "PostgreSQL started"

python manage.py migrate

gunicorn --bind 0.0.0.0:80 api.wsgi
