#!/bin/bash

gunicorn --workers=2 --bind=0.0.0.0:8000 mysite.wsgi:application
python manage.py migrate
# python manage.py collectstatic — noinput