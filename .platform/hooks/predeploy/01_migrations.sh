#!/bin/bash

source /var/app/venv/*/bin/activate
cd /var/app/staging

python3 manage.py migrate
