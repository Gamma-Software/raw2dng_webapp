#!/bin/bash
python project/manage.py makemigrations raw2dng;
python project/manage.py migrate raw2dng --noinput;
python project/manage.py migrate --noinput;
python project/manage.py runserver 0.0.0.0:8000;