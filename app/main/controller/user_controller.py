from flask_restx import Resource, Api, Namespace
from ..model.user import api
from ..model.user import UserDto
from ..service.user_service import get_all_users, save_new_user, get_a_user, update_user, delete_user
from typing import Tuple, Dict

from flask import request

_user = UserDto.user
_user_out = UserDto.user_out


@api.route('/')
class UserController(Resource):
    @api.doc('list_of_students')
    @api.marshal_list_with(_user_out, envelope='data')
    def get(self):
        return get_all_users()

    @api.expect(_user, validate=True)
    @api.response(201, 'User successfully created.')
    @api.marshal_with(_user_out)
    @api.doc('create a new User')
    def post(self) -> Tuple[Dict[str, str], int]:
        data = request.json
        return save_new_user(data=data)


@api.route('/<id>')
@api.param('id', 'The User identifier')
@api.response(404, 'User not found.')
class OneUserController(Resource):
    @api.doc('get a user')
    @api.marshal_with(_user_out)
    def get(self, id):
        user = get_a_user(id)
        print(user)
        if not user:
            api.abort(404)
        else:
            return user

    @api.expect(_user, validate=True)
    @api.response(201, 'User successfully updated.')
    @api.marshal_with(_user_out)
    @api.doc('update a User')
    def put(self, id) -> Tuple[Dict[str, str], int]:
        data = request.json
        return update_user(id, data)

    @api.response(204, 'User successfully deleted.')
    @api.doc('delete a new User')
    def delete(self, id) -> Tuple[Dict[str, str], int]:
        delete_user(id)
        return {'status': 'DELETED'}, 204