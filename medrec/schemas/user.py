from marshmallow import (
    fields,
    validate,
    post_load
)

from medrec.extensions import ma
from medrec.models import Users
from .base import ObjectId


class UserSchema(ma.Schema):
    id = ObjectId(dump_only=True)
    username = ma.String(required=True)
    email = ma.String(required=True,
                      validate=validate.Email(
                          error='Not a valid email address'))
    password = ma.String(load_only=True, required=True)
    created_on = ma.DateTime(dump_only=True)

    @post_load
    def make_user(self, data):
        return Users(**data)
