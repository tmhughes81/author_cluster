#!/bin/bash
cd /code
/usr/bin/python /code/acp/manage.py migrate
/usr/bin/python /code/acp/manage.py runserver 0.0.0.0:8000
