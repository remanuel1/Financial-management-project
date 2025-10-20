from flask_restx import Resource
from ..model.user import api

@api.route('/')
class UserController(Resource):
    @api.doc('Hello world')
    def get(self):
        return "Hello world"