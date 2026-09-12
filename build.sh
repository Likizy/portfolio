#!/usr/bin/env bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

# Set these variables in Render only when creating the first administrator:
# DJANGO_ADMIN_USERNAME, DJANGO_ADMIN_EMAIL, and DJANGO_ADMIN_PASSWORD.
if [ -n "${DJANGO_ADMIN_USERNAME:-}" ] && [ -n "${DJANGO_ADMIN_PASSWORD:-}" ]; then
  python manage.py create_admin
fi
