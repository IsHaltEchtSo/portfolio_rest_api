from rest_api.models import User
from marshmallow import Schema, fields, post_load

class UserSchema(Schema):
    name = fields.String()
    age = fields.Integer()
    follower = fields.List(fields.Nested('UserSchema'), default=[])
    following = fields.List(fields.Nested('UserSchema'), default=[])

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)