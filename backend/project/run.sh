#!/bin/sh
python project/manage.py makemigrations raw2dng;
python project/manage.py migrate raw2dng;
python project/manage.py migrate;
python project/manage.py runserver;