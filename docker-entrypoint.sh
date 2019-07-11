#!/bin/bash

gunicorn --workers=2 --bind=0.0.0.0:8000 mysite.wsgi:application

# Apply database migrations
# echo "Apply database migrations"
# python manage.py migrate

# Start server
# echo "Starting server"
# python manage.py runserver 0.0.0.0:8000

# gunicorn --workers=2 --bind=0.0.0.0:8000 mysite.wsgi:application
# python manage.py migrate
# python manage.py collectstatic — noinput