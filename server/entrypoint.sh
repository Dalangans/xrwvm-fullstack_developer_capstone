#!/bin/sh
# Make migrations and migrate the database.
echo "Making migrations and migrating the database. "
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Create superuser if not exists
echo "Creating superuser..."
python manage.py shell << END
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@admin.com', 'admin')
    print('Superuser admin created')
else:
    print('Superuser admin already exists')
END

# Populate database with test data
echo "Populating database with test data..."
python manage.py shell << END
import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproj.settings')

from djangoapp.populate import initiate_data
initiate_data()
END

exec "$@"
