#!/bin/bash
export PYTHONPATH=/usr/local/lib/python2.7/site-packages

/usr/bin/python /code/acp/manage.py migrate
/usr/bin/python /code/acp/manage.py runserver 0.0.0.0:8000
