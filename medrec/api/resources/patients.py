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
    DoesNotExist, NotUniqueError, ValidationError
)
import pyqrcode
import png
import os
conf = loadconf()


class Patients(JWTResource):

    def get(self):
        schema = PatientsSchema(many=True)
        data = request.args

        patients = PatientsModel.objects(added_by=get_current_user())
        return paginate(patients, schema)

    def post(self):

        schema = PatientsSchema()
        data = request.json
        patient, errors = schema.load(data)

        if errors:
            return errors, 422

        patient.added_by = get_current_user()

        try:
            patient.save()
            patient_id = str(patient.id)

            patient_qr = pyqrcode.create(patient_id)
            loc = os.path.join(conf.QR_DIR, 'patient_%s.png' % patient_id)
            patient_qr.png(loc, scale=8)
        except NotUniqueError as e:
            return make_response(
                jsonify(message="The name already exists"), 409
            )

        return schema.jsonify(patient)


class Patient(JWTResource):

    def get(self, pid):

        schema = PatientsSchema()

        patient = PatientsModel.objects.get_or_404(
            id=pid, added_by=get_current_user())

        return schema.jsonify(patient)

    def put(self, pid):

        schema = PatientsSchema(partial=True)
        data = request.json
        patient = PatientsModel.objects.get_or_404(
            id=pid, added_by=get_current_user())
        name = data.get('name')
        description = data.get('description')
        medication = data.get('medication')

        if data:
            _, errors = schema.load(data)

            if errors:
                return errors, 422

            if name:
                patient.name = name
            if description:
                patient.description = description
            if medication:
                patient.medication = medication

            patient.save()

        return schema.jsonify(patient)

    def delete(self, pid):

        patient = PatientsModel.objects.get_or_404(
            id=pid, added_by=get_current_user())

        patient.delete()

        return {'message': 'Patient deleted'}
