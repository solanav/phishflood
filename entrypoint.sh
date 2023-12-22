#!/bin/bash

echo "Making migrations..."
poetry run python manage.py makemigrations phishings --noinput

echo "Migrating..."
poetry run python manage.py migrate --noinput

echo "Collecting static files..."
poetry run python manage.py collectstatic --noinput

echo "Creating admin user..."
echo "from django.contrib.auth.models import User; User.objects.filter(email='admin@phishflood.com').delete(); User.objects.create_superuser('admin', 'admin@phishflood.com', 'dhZpZz4*a8kw#Y#t')" | poetry run python manage.py shell

echo "Runnning gunicorn..."
poetry run gunicorn phishing_analyzer.wsgi:application -w 8 --bind 0.0.0.0:8000