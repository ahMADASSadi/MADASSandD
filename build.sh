#!/bin/bash

# Install dependencies
pip install -r requirements.txt
pip install pymemcache

# Run Django migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Compile translation messages if needed
python manage.py compilemessages