import pytest

from flask import Flask

def flask_app_mock():
    app_mock = Flask(__name__)
    return app_mock