from flask_restx import Resource, Api, Namespace
from ..model.user_expense import api, UserExpenseDto
from ..service.user_expense_service import *
from typing import Tuple, Dict

from flask import request

_user_expense = UserExpenseDto.user_expense
_user_expense_out = UserExpenseDto.user_expense_out

@api.route('/<int:user_id>/expenses')
@api.param('user_id', 'The User identifier')
class UserExpenseController(Resource):
    @api.doc('list_expenses_for_user')
    @api.marshal_list_with(_user_expense_out, envelope='data')
    def get(self, user_id):
        """
        Get all expenses for a user, or by date range if query params provided.
        Example: GET /user_expense/1/expenses?start=2025-01-01&end=2025-01-31
        """
        start_date = request.args.get('start')
        end_date = request.args.get('end')

        if start_date and end_date:
            return get_expenses_for_user_in_date_range(user_id, start_date, end_date)
        else:
            return get_all_expenses_for_user(user_id)

    @api.expect(_user_expense, validate=True)
    @api.response(201, 'Expense successfully created.')
    @api.marshal_with(_user_expense_out)
    @api.doc('create a new expense for a user')
    def post(self, user_id):
        """Create a new expense for the user"""
        data = request.json
        data['user_id'] = user_id  # attach the user ID from path
        return save_new_user_expense(user_id, data)

@api.route('/<int:user_id>/expenses/<int:expense_id>')
@api.param('user_id', 'The User identifier')
@api.param('expense_id', 'The Expense identifier')
@api.response(404, 'User not found.')
class OneUserExpenseController(Resource):

    @api.expect(_user_expense, validate=True)
    @api.response(200, 'Expense successfully updated.')
    @api.marshal_with(_user_expense_out)
    @api.doc('update an expense for a user')
    def put(self, user_id, expense_id):
        """Update an existing expense for a specific user"""
        data = request.json
        return update_user_expense(expense_id, data)


    @api.response(204, 'User expense successfully deleted.')
    @api.doc('delete a User expense')
    def delete(self, user_id, id) -> Tuple[Dict[str, str], int]:
        delete_user_expense(id)
        return {'status': 'DELETED'} , 204

    @api.response(204, 'Expense successfully deleted.')
    @api.doc('delete an expense for a user')
    def delete(self, user_id, expense_id):
        """Delete an expense for a specific user"""
        return delete_user_expense(user_id, expense_id)