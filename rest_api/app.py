from flask import Flask
from flask_restful import Api

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile(filename='config.py')
    
    with app.app_context():
        from rest_api.resources import UsersResource

        api = Api(app=app)

        # registration of api resources
        api.add_resource(UsersResource, '/users', endpoint='users_ep')

    return app
