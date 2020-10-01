#!/bin/bash
# wait for Postgres to start
# wait for Postgres to start
function postgres_ready() {
python << END
import sys
import os
import psycopg2
try:
    conn = psycopg2.connect(dbname=os.environ.get('POSTGRES_DB'),
    user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD'), host=os.environ.get('POSTGRES_HOST'))
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

# Start app
>&2 echo "Postgres is up - executing command"

/usr/sbin/sshd

# Update database
python manage.py migrate

# Copy static files to STATIC_ROOT
python manage.py collectstatic --noinput

# Start server
gunicorn wsgi -w 4 -b 0.0.0.0:80 --chdir=/code/app --log-file -