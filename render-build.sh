#!/usr/bin/env bash

echo "🛠️ Applying migrations..."
python manage.py makemigrations
python manage.py migrate
