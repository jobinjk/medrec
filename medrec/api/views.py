from flask import Blueprint
from flask_restful import Api

from qa.api.resources import (
    User,
    Users
)

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint)


api.add_resource(User, '/users/<uid>')
api.add_resource(Users, '/users')
