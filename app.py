from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile(filename='rest_api/config.py')

    return app
