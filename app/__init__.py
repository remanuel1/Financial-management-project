from flask_restx import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.user_expense_controller import api as user_expense_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='USER APP',
          version='1.0',
          description='flask restplus web service for financial managment'
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(user_expense_ns, path='/user')