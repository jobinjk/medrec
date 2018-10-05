from flask_restful import Resource
from flask_jwt_extended import jwt_required


class JWTResource(Resource):
    method_decorators = [jwt_required]
