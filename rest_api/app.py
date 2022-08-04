from flask import Flask
from flask_restful import Api



def create_app():
    app = Flask(__name__)

    try:
        app.config.from_pyfile(filename='config.py')
        
        app_initializer = AppInitializer(app=app)
        app_initializer.init_app()

        return app
    except Exception as ex:
        raise ex


class AppInitializer:
    def __init__(self, app: Flask) -> None:
        self.flask_app = app
        self.config = app.config


    def init_views(self) -> None:
        """
        Uses local imports because some models in turn import the flask app
        This is called with an app context to to avoid context errors
        """
        from rest_api.resources import UsersResource, UserResource, FollowingResource, FollowerResource

        api = Api(app=self.flask_app)

        api.add_resource(UsersResource, '/users', endpoint='users_ep')
        api.add_resource(UserResource, '/user/<int:user_id>', endpoint='user_ep')
        api.add_resource(FollowingResource, '/following', endpoint='following_ep')
        api.add_resource(FollowerResource, '/follower', endpoint='follower_ep')


    def init_app_in_ctx(self) -> None:
        """
        Runs init logic in the context of the app
        """
        self.init_views()


    def init_app(self) -> None:
        """
        Main entry point which will delegate to other methods
        in order to fully initialize the app
        """
        with self.flask_app.app_context():
            self.init_app_in_ctx()
