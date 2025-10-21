from flask_restx import Namespace, fields

api = Namespace('user_expense', description='user expense related operations')

from .. import db

class UserExpense(db.Model):
    __tablename__ = "user_expense"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    store_name = db.Column(db.String(255), nullable=False)
    total_sum = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "<user expense'{} {}'>".format(self.user_id, self.store_name)


class UserExpenseDto:
    user_expense = api.model('user_expense', {
        'user_id': fields.Integer(required=True, description='User ID related to the expense'),
        'date': fields.Date(required=True, description='Date of the expense'),
        'store_name': fields.String(required=True, description='Store name from the invoice'),
        'total_sum': fields.Float(required=True, description='Total expense amount'),
        'category': fields.String(required=True, description='Expense category')
    })

    user_expense_out = api.model('user_expense_out', {
        'id': fields.Integer(description='Expense ID'),
        'created_at': fields.Date(description='When the record was created'),
        'user_id': fields.Integer(description='User ID related to the expense'),
        'date': fields.Date(description='Date of the expense'),
        'store_name': fields.String(description='Store name from the invoice'),
        'total_sum': fields.Float(description='Total expense amount'),
        'category': fields.String(description='Expense category')
    })
