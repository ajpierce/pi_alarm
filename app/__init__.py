import os

from flask import Flask
from flask.ext.basicauth import BasicAuth

app = Flask(__name__, static_folder='static')
app.config.from_object('config')
app.secret_key = 'forms will submit properly now'

basic_auth = BasicAuth(app)

from app import controller
