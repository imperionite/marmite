#!/usr/bin/env bash
# Exit on error
set -o errexit

# Dynamically set PROJECT_ROOT using pwd for local development
PROJECT_ROOT=$(pwd)

# Set the Django settings module
export DJANGO_SETTINGS_MODULE=core.settings

# Collect static files
python $PROJECT_ROOT/connectly-api/manage.py collectstatic --no-input

# Apply database migrations
python $PROJECT_ROOT/connectly-api/manage.py migrate --no-input

# Run the custom command to create a superuser
python $PROJECT_ROOT/connectly-api/manage.py create_superuser

# Generate fixture data
python $PROJECT_ROOT/connectly-api/manage.py generate_fixture_data

# Run the custom management command to assign roles and groups
python $PROJECT_ROOT/connectly-api/manage.py assign_roles
