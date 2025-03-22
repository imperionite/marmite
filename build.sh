#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Collect static files (needed for Django Admin and any other static assets)
python connectly-api/manage.py collectstatic --no-input

# Apply database migrations
python connectly-api/manage.py migrate --no-input

# Run the custom command to create a superuser
python connectly-api/manage.py create_superuser

# Generate fixture data (if you want fresh generated data each time)
python connectly-api/manage.py generate_fixture_data

# Run the custom management command to assign roles
python connectly-api/manage.py assign_roles

