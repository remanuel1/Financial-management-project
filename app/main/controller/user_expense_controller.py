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
    #@api.param(name='user_id', description='Filter by user ID')
    @api.param(name='start', description='Start date (YYYY-MM-DD)')
    @api.param(name='end', description='End date (YYYY-MM-DD)')
    @api.param(name='store_name', description='Filter by store name')
    @api.param(name='category', description='Filter by category')
    @api.param(name='orderby_field', description='Field to order by')
    @api.param(name='orderby_direction', description='Order direction')
    @api.param(name='page', description='Page number', default=1)
    @api.param(name='count', description='Items per page', default=50)
    # @api.marshal_list_with(_user_expense_out, envelope='data')
    def get(self, user_id):
        # Parse query parameters
        page = request.args.get("page")
        if page:
            page = int(page)
        count = request.args.get("count")
        if count:
            count = int(count)

        start = request.args.get("start")
        end = request.args.get("end")
        store_name = request.args.get("store_name")
        category = request.args.get("category")

        orderby_field = request.args.get("orderby_field")
        orderby_direction = request.args.get("orderby_direction")

        return get_all_expenses(
            user_id=user_id,\
            start_date=start,\
            end_date=end,\
            store_name=store_name,\
            category=category,\
            orderby_field=orderby_field,\
            orderby_direction=orderby_direction,\
            page=page,\
            count=count
        )

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