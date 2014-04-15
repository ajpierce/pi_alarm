#!/bin/bash

# -- This script starts the server on port that nginx knows to monitor
# -- See the nginx_config file for "details"

uwsgi --socket 127.0.0.1:3031 -w app:app \
    --master \
    --processes 2 --threads 1
