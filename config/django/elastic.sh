#!/bin/bash
set -e

# Wait for elastic search to start before indexing
function elastic_ready() {
URL=http://elasticsearch:9200/_cat/health?h=st
STATUS_CODE=$(curl --write-out %{http_code} --silent --output /dev/null $URL)
  echo "Elasticsearch status code: $STATUS_CODE"

  if [ $STATUS_CODE -eq "200" ]; then
    return 0
  else
    return 1
  fi
}

until elastic_ready; do
  >&2 echo "Elastic search unavailable - sleeping"
  sleep 10
done

# Start app
>&2 echo "Elastic search is up - executing command"

black --check . --config pyproject.toml

isort --check-only .

flake8

python manage.py makemigrations --check

pytest