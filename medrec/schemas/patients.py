from marshmallow import (
    fields,
    validate,
    post_load
)

from medrec.extensions import ma
from .user import UserSchema
from .base import ObjectId
from medrec.models import Patients


class PatientsSchema(ma.Schema):

    id = ObjectId(dump_only=True)
    name = ma.String(required=True)
    description = ma.String(required=True)
    medication = ma.List(ma.String, required=True)
    added_by = ma.Nested(UserSchema, dump_only=True)
    created_on = ma.DateTime(dump_only=True)

    @post_load
    def make_patient(self, data):
        return Patients(**data)
