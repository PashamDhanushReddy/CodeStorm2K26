#!/bin/bash
set -o errexit

# Upgrade pip and install build tools
pip install --upgrade pip setuptools wheel

# Install requirements
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input