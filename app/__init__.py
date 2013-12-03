import os

from flask import Flask
from flask.ext.basicauth import BasicAuth

app = Flask(__name__, static_folder='static')
app.config.from_object('config')

basic_auth = BasicAuth(app)

from app import controller
