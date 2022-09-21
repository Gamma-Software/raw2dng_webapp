#!/bin/bash
python project/manage.py makemigrations raw2dng;
python project/manage.py migrate raw2dng;
python project/manage.py migrate;
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | python project/manage.py shell