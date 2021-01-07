import os

from flask import Flask
from . import xkcd

PORT = (
    5000
    if not isinstance(os.environ.get("FLASK_PORT"), int)
    else os.environ.get("FLASK_PORT")
)
HOST = (
    "127.0.0.1"
    if os.environ.get("FLASK_HOST") is None
    else os.environ.get("FLASK_HOST")
)


def create_app():
    app = Flask(__name__)

    app.register_blueprint(xkcd.bp)

    return app
