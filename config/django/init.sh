#!/bin/bash
set -e

# wait for Postgres to start
# wait for Postgres to start
function postgres_ready() {
python << END
import sys
import os
import psycopg2
try:
    conn = psycopg2.connect(dbname=os.environ.get('POSTGRES_DB'),
    user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD'),
    host=os.environ.get('POSTGRES_HOST'))
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

echo "Starting SSH ..."
service ssh start

python manage.py migrate

python manage.py collectstatic --noinput --clear

chmod -R u=rwX,g=rwX,o=rX /home/site/wwwroot/staticfiles/

gunicorn wsgi -w 4 -b 0.0.0.0:8000 --chdir=/home/site/wwwroot/app --log-file -