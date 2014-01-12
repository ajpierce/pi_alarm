import os
basedir = os.path.abspath(os.path.dirname(__file__))

# -- Light Config
PIN = 10
ON_DURATION = 15    # in minutes

# -- General Config
DEBUG = True
CSRF_ENABLED = True
BASIC_AUTH_FORCE = False
BASIC_AUTH_USERNAME = 'alarm'
BASIC_AUTH_PASSWORD = 'password'
