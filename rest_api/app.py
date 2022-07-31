from flask import Flask
from rest_api.schemas import UserSchema

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile(filename='config.py')

    return app
