#!/bin/bash
set -e

echo "Starting SSH ..."
service ssh start

python manage.py migrate
python manage.py runserver 0.0.0.0:8000

gunicorn --bind 0.0.0.0:80 app.wsgi