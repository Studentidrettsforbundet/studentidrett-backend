#!/bin/bash
set -e

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

## Wait for elastic search to start before indexing
#function elastic_ready() {
#URL=http://elasticsearch:9200/_cat/health?h=st
#STATUS_CODE=$(curl --write-out %{http_code} --silent --output /dev/null $URL)
#  echo "Elasticsearch status code: $STATUS_CODE"
#
#  if [ $STATUS_CODE -eq "200" ]; then
#    return 0
#  else
#    return 1
#  fi
#}

until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

#until elastic_ready; do
#  >&2 echo "Elastic search unavailable - sleeping"
#  sleep 10
#done

# Start app
>&2 echo "Postgres and Elastic search is up - executing command"

python manage.py migrate

python manage.py collectstatic --noinput --clear

# python manage.py search_index --rebuild -f

chmod -R u=rwX,g=rwX,o=rX /staticfiles/

gunicorn wsgi -w 4 -b 0.0.0.0:8000 --chdir=/code/app --log-file -