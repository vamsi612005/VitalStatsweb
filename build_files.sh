#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Create a virtual environment and activate it
python3 -m venv venv
source venv/bin/activate

# Upgrade pip to the latest version
pip install --upgrade pip

# Install the required dependencies
pip install -r requirements.txt

# Collect static files (if needed)
python manage.py collectstatic --noinput

# Run database migrations
# python manage.py migrate

