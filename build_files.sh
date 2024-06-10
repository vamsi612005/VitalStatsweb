#!/bin/bash

# Install Python dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run database migrations and collect static files (if needed)
python manage.py migrate
python manage.py collectstatic --noinput
