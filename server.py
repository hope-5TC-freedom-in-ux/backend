from flask import Flask, session, redirect
from flask_restplus import Api
from random import choice
import os

import toml

from conf.secrets import session_key

from api import blueprint
from game import game

app = Flask(__name__)
app.register_blueprint(blueprint)
app.register_blueprint(game, url_prefix='/')
app.secret_key = session_key

if __name__ == "__main__":
    app.run(debug=True)
