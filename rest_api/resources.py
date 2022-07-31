from sqlalchemy import desc
from rest_api.models import Session, User
from rest_api.schemas import UserSchema

from flask import request
from flask_restful import Resource

#TODO add type hints for resource methods
class UsersResource(Resource):

    def get(self):
        """GET all users"""
        session = Session()

        user_object_list = session.query(User).all()
        user_object_list_serialized = UserSchema().dump(user_object_list, many=True)

        return user_object_list_serialized

    def post(self):
        """CREATE a new user"""
        new_user_object = UserSchema().load(data=request.form)
        
        session = Session()
        session.add(new_user_object)
        session.commit()

        new_user_object_serialized = UserSchema().dump(new_user_object)
        return new_user_object_serialized


class UserResource(Resource):

    def get(self, user_id):
        """GET a user by id"""
        session = Session()

        user_object = session.query(User).get(user_id)

        if user_object:
            user_object_serialized = UserSchema().dump(user_object)

            return user_object_serialized

        return None


    def patch(self, user_id):
        """UPDATE a user by id"""
        session = Session()

        user_object = session.query(User).get(user_id)

        if user_object:

            if request.form.get('name'):
                user_object.name = request.form['name']
            
            if request.form.get('age'):
                user_object.age = request.form['age']

            session.add(user_object)
            session.commit()

        user_object_serialized = UserSchema().dump(user_object)

        return user_object_serialized


    def delete(self, user_id):
        """DELETE a user by id"""
        session = Session()

        user_object = session.query(User).get(user_id)

        if user_object:
            session.delete(user_object)
            session.commit()

        user_object_serialized = UserSchema().dump(user_object)

        return user_object_serialized


class FollowingResource(Resource):

    def get(self):
        """GET all users ordered by following_count in descending order"""
        session = Session()

        user_object_list = session.query(User).order_by(desc(User.following_count)).all()
        user_object_list_serialized = UserSchema().dump(user_object_list, many=True)

        return user_object_list_serialized


    def patch(self):
        """UPDATE a user with a new following"""
        session = Session()

        follower_id, followee_id = request.form.get('follower_id'), request.form.get('followee_id')
        follower_user_object = session.query(User).get(follower_id)
        followee_user_object = session.query(User).get(followee_id)

        if follower_user_object and followee_user_object:
            follower_user_object.following.append(followee_user_object)
            session.add(follower_user_object)
            session.commit()

        follower_user_object_serialized = UserSchema().dump(follower_user_object)
        return follower_user_object_serialized





class FollowerResource(Resource):

    def get(self):
        """GET all users ordered by follower_count in descending order"""
        session = Session()

        user_object_list = session.query(User).order_by(desc(User.follower_count)).all()
        user_object_list_serialized = UserSchema().dump(user_object_list, many=True)

        return user_object_list_serialized

    #TODO delete patch, does not make sense to choose someone as your follower
    def patch(self):
        """UPDATE a user with a new follower"""
        session = Session()

        follower_id, followee_id = request.form.get('follower_id'), request.form.get('followee_id')
        follower_user_object = session.query(User).get(follower_id)
        followee_user_object = session.query(User).get(followee_id)

        if follower_user_object and followee_user_object:
            followee_user_object.follower.append(follower_user_object)

        session.add(followee_user_object)
        session.commit()

        followee_user_object_serialized = UserSchema().dump(followee_user_object)

        return followee_user_object_serialized
