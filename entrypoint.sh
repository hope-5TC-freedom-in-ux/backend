#!/bin/bash

exec gunicorn server:app \
    --bind 0.0.0.0:8000 \
    --workers 2

"$@"
