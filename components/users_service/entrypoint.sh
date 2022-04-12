#!/usr/bin/env sh

gunicorn --bind 0.0.0.0:1234 run:app --reload -w 1