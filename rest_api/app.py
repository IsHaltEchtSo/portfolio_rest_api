from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile(filename='config.py')
    
    with app.app_context():
        from rest_api.schemas import UserSchema

    return app
