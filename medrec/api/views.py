from flask import Blueprint
from flask_restful import Api

from medrec.api.resources import (
    User,
    Users,
    ProfileResource,
    Patient,
    Patients
)

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint)


api.add_resource(User, '/users/<uid>')
api.add_resource(Users, '/users')
api.add_resource(ProfileResource, '/users/profile')

api.add_resource(Patient, '/patients/<pid>')
api.add_resource(Patients, '/patients')
