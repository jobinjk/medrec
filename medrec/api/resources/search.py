from .base import JWTResource
from flask import jsonify, request, make_response
from flask_jwt_extended import get_current_user
from medrec.schemas import PatientsSchema
from medrec.models import (
    Patients as PatientsModel,
    Users
)
from medrec.helpers import (
    paginate,
    loadconf
)
from mongoengine.errors import (
    DoesNotExist, ValidationError
)

import os
conf = loadconf()


class Search(JWTResource):

    def get(self):

        schema = PatientsSchema()
        data = request.args
        current_user = get_current_user()

        pid = data.get('id')

        try:
            patient = PatientsModel.objects.get(id=pid)

        except (DoesNotExist, ValidationError):
            return make_response(
                jsonify(message='Patient not found'),
                404
            )

        return schema.jsonify(patient)
