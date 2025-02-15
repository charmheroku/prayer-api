#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements/prod.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Load fixtures
python manage.py loaddata fixtures/initial_data.json 