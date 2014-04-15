#!/bin/bash
# --
# Script to install python packages needed to run pi_alarm
# Note that you may need to run this script as root
# --

# Required Python Libraries
python_libs=(
    'flask==0.10.1'             # The web framework we're using
    'Mako==0.9.0'               # Mako templates for the site
    'flask-mako'                # Flask integration for Mako
    'uwsgi'                     # for serving the site
    'Flask-BasicAuth'           # for locking down the site
    'python-crontab'            # for accessing the crontab
)

# Install each of the libraries
for i in "${python_libs[@]}"; do
    pip install $i
done
