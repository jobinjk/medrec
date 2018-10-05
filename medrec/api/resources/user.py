from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import get_current_user

from medrec.models import (
    Users as UserModal
)
from medrec.schemas import UserSchema
from medrec.extensions import db
from .base import JWTResource
from mongoengine import Q


class User(JWTResource):

    def get(self, uid):
        schema = UserSchema()

        if not request.is_json:
            return jsonify({'msg': 'Missing JSON in request'}), 400

        user = UserModal.objects.get_or_404(id=uid)
        return schema.jsonify(user)

    def patch(self, uid):
        schema = UserSchema(partial=True)

        if not request.is_json:
            return jsonify({'msg': 'Missing JSON in request'}), 400

        user = UserModal.objects.get_or_404(id=uid)

        user, errors = schema.load(request.json)
        if errors:
            return errors, 422

        user.save()
        return schema.jsonify(user)

    def delete(self, uid):
        user = UserModal.objects.get_or_404(id=uid)

        return {'msg': 'User deleted'}


class Users(JWTResource):

    def get(self):
        schema = UserSchema(many=True)

        users = UserModal.objects()

        return paginate(users, schema)

    def post(self):
        schema = UserSchema()

        user, errors = schema.load(request.json)
        if errors:
            return errors, 422

        user.save()

        return schema.jsonify(user)
