#!/bin/bash
set -e
cmd="$@"

# This entrypoint is used to play nicely with the current cookiecutter configuration.
# Since docker-compose relies heavily on environment variables itself for configuration, we'd have to define multiple
# environment variables just to support cookiecutter out of the box. That makes no sense, so this little entrypoint
# does all this for us.
export REDIS_URL=redis://redis:6379

# the official postgres image uses 'postgres' as default user if not set explictly.
if [ -z "$POSTGRES_USER" ]; then
    export POSTGRES_USER=postgres
fi

export DATABASE_URL=postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@$PGBOUNCER_HOST:$PGBOUNCER_PORT/$POSTGRES_USER

export CELERY_BROKER_URL=$REDIS_URL/0

function pgbouncer_ready(){
python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(dbname="$POSTGRES_USER", user="$POSTGRES_USER", password="$POSTGRES_PASSWORD", host="$PGBOUNCER_HOST", port="$PGBOUNCER_PORT")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

function postgres_ready(){
python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(dbname="$POSTGRES_USER", user="$POSTGRES_USER", password="$POSTGRES_PASSWORD", host="$POSTGRES_HOST", port="$POSTGRES_PORT")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until pgbouncer_ready; do
  >&2 echo "PGBouncer is unavailable - sleeping"
  sleep 1
done

until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres and PGBouncer is up - continuing..."
exec $cmd
