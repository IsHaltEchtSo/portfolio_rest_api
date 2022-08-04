from sqlalchemy import desc
from rest_api.models import Session, UserModel
from rest_api.schemas import UserSchema

from flask import request
from flask_restful import Resource


class UsersResource(Resource):
    def get(self) -> str:
        """GET all users"""
        session = Session()

        user_object_list = session.query(UserModel).all()
        user_object_list_serialized = UserSchema().dump(user_object_list, many=True)

        return user_object_list_serialized


    def post(self) -> str:
        """CREATE a new user"""
        new_user_object = UserSchema().load(data=request.form)
        
        session = Session()
        session.add(new_user_object)
        session.commit()

        new_user_object_serialized = UserSchema().dump(new_user_object)
        return new_user_object_serialized


class UserResource(Resource):
    def get(self, user_id) -> str:
        """GET a user by id"""
        session = Session()

        user_object = session.query(UserModel).get(user_id)

        if user_object:
            user_object_serialized = UserSchema().dump(user_object)

            return user_object_serialized

        return None


    def patch(self, user_id) -> str:
        """UPDATE a user by id"""
        session = Session()

        user_object = session.query(UserModel).get(user_id)

        if user_object:

            if request.form.get('name'):
                user_object.name = request.form['name']
            
            if request.form.get('age'):
                user_object.age = request.form['age']

            session.add(user_object)
            session.commit()

        user_object_serialized = UserSchema().dump(user_object)

        return user_object_serialized


    def delete(self, user_id) -> str:
        """DELETE a user by id"""
        session = Session()

        user_object = session.query(UserModel).get(user_id)

        if user_object:
            session.delete(user_object)
            session.commit()

        user_object_serialized = UserSchema().dump(user_object)

        return user_object_serialized


class FollowingResource(Resource):
    def get(self) -> str:
        """GET all users ordered by following_count in descending order"""
        session = Session()

        user_object_list = session.query(UserModel).order_by(desc(UserModel.following_count)).all()
        user_object_list_serialized = UserSchema().dump(user_object_list, many=True)

        return user_object_list_serialized


    def patch(self) -> str:
        """UPDATE a user with a new following"""
        session = Session()

        follower_id, followee_id = request.form.get('follower_id'), request.form.get('followee_id')
        follower_user_object = session.query(UserModel).get(follower_id)
        followee_user_object = session.query(UserModel).get(followee_id)

        if follower_user_object and followee_user_object:
            follower_user_object.following.append(followee_user_object)
            session.add(follower_user_object)
            session.commit()

        follower_user_object_serialized = UserSchema().dump(follower_user_object)
        return follower_user_object_serialized


class FollowerResource(Resource):
    def get(self) -> str:
        """GET all users ordered by follower_count in descending order"""
        session = Session()

        user_object_list = session.query(UserModel).order_by(desc(UserModel.follower_count)).all()
        user_object_list_serialized = UserSchema().dump(user_object_list, many=True)

        return user_object_list_serialized
