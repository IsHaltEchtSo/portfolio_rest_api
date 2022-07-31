from flask_restful import Resource


class UsersResource(Resource):

    def get(self):
        """GET all users"""
        pass

    def post(self):
        """CREATE a new user"""
        pass


class UserResource(Resource):

    def get(self, user_id):
        """GET a user by id"""
        pass

    def patch(self, user_id):
        """UPDATE a user by id"""
        pass

    def delete(self, user_id):
        """DELETE a user by id"""
        pass


class FollowingResource(Resource):

    def get(self):
        """GET all users ordered by following_count in descending order"""
        pass


class FollowerResource(Resource):

    def get(self):
        """GET all users ordered by follower_count in descending order"""