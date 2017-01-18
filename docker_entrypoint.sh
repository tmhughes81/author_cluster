#!/bin/bash

export PYTHONPATH=/usr/local/lib/python2.7/site-packages:/code/acp

/usr/bin/python /code/acp/manage.py migrate
/usr/bin/python /code/acp/manage.py collectstatic --noinput  # Collect static files

# Prepare log files and start outputting logs to stdout
touch /srv/logs/gunicorn.log
touch /srv/logs/access.log
tail -n 0 -f /srv/logs/*.log &

# Start Gunicorn processes
echo Starting Gunicorn.

exec gunicorn wsgi:application \
    --name acp \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --log-level=info \
    --log-file=/srv/logs/gunicorn.log \
    --access-logfile=/srv/logs/access.log \
    --preload \
    "$@"
