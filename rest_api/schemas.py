from rest_api.models import User
from marshmallow import Schema, fields, post_load

class UserSchema(Schema):
    class Meta:
        ordered = True
        
    id = fields.Integer(default=None)
    name = fields.String()
    age = fields.Integer()
    follower = fields.List(fields.Nested('UserSchema', exclude=['follower', 'following']), default=[])
    following = fields.List(fields.Nested('UserSchema', exclude=['follower', 'following']), default=[])

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)