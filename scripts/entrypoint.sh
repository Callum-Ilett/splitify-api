#!/bin/sh

# Set working directory
cd src

if [ "$ENVIRONMENT" = "development" ]; then
    # Run Django development server
    python -Xfrozen_modules=off manage.py runserver 0.0.0.0:8000
else
    # Migrate database
    python manage.py migrate

    # Collect static files
    python manage.py collectstatic --noinput

    # Run Gunicorn production server
    gunicorn core.wsgi:application --bind 0.0.0.0:8000
fi