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

# --------For Profile View---------


class ProfileResource(JWTResource):

    def get(self):
        schema = UserSchema(partial=True)

        current_user = get_current_user()
        try:
            if current_user:
                profile = UserModal.objects.get(id=str(current_user.id))
            else:
                raise DoesNotExist
        except DoesNotExist:
            return make_response(
                jsonify(message='Profile not found'), 404
            )

        profile = schema.dump(profile).data

        return jsonify(
            profile=profile
        )

    def put(self):

        data = request.get_json()
        password = data.get('password')
        current_user = get_current_user()
        schema = UserSchema()

        try:
            if current_user:
                profile = UserModal.objects.get(id=current_user.id)
            else:
                raise DoesNotExist
        except DoesNotExist as e:
            return make_response(
                jsonify(message='Profile Not Found'),
                404
            )
        if password:
            old = password.get('old', '')
            new = password.get('new', '')
            if old and new:
                if old == new:
                    return make_response(
                        jsonify(message='Password is same'),
                        400
                    )
                if len(new) < 5:
                    return make_response(
                        jsonify(message='Password too short'),
                        400
                    )
                if not profile.change_password(old, new):
                    return make_response(
                        jsonify(
                            message='Old password is invalid, unable to authenticate'),
                        409
                    )
                profile.save()
        profile.reload()
        return schema.jsonify(profile)
