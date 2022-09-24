#!/bin/sh
python project/manage.py createsuperuser --noinput;
python project/manage.py makemigrations raw2dng  --noinput;
python project/manage.py migrate raw2dng --noinput;
python project/manage.py migrate --noinput;
python project/manage.py runserver 0.0.0.0:8000;