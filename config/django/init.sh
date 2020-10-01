#!/bin/bash
set -e

echo "Starting SSH ..."
service ssh start

python app/manage.py migrate
python app/manage.py runserver 0.0.0.0:8000

gunicorn --bind 0.0.0.0:80 app.wsgi