import datetime
from app.main import db
from app.main.model.user import User
from app.main.model.user_expense import UserExpense
from typing import Dict, Tuple


def save_new_user_expense(user_id, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    # check if user exists
    user = User.query.filter_by(id=user_id).first()
    if user:
        new_user_expense = UserExpense(
            created_at=datetime.datetime.utcnow(),
            user_id=data['user_id'],
            date=data['date'],
            store_name=data['store_name'],
            total_sum=data['total_sum'],
            category=data['category']
        )
        return save_changes(new_user_expense), 201

    else:
        response_object = {
            'status': 'fail',
            'message': 'User does not exist.',
        }
        return response_object, 409


def update_user_expense(id: int, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    user_expense = db.session.query(UserExpense).filter_by(id=id).first()
    if user_expense:
        user_expense.date = data['date'],
        user_expense.store_name = data['store_name'],
        user_expense.total_sum = data['total_sum'],
        user_expense.category = data['category']

        db.session.commit()
        return user_expense, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'user expense not found',
        }
        return response_object, 409


def get_all_expenses_for_user(user_id: int):
    return UserExpense.query.filter(UserExpense.user_id == user_id).all()

def get_expenses_for_user_in_date_range(user_id: int, start_date: datetime, end_date: datetime):

    return UserExpense.query.filter(
        UserExpense.user_id == user_id,
        UserExpense.date >= start_date,
        UserExpense.date <= end_date
    ).all()


def delete_user_expense(user_id: int, expense_id: int) -> Tuple[Dict[str, str], int]:
    user_expense = db.session.query(UserExpense).filter(
        UserExpense.user_id == user_id,
        UserExpense.id == expense_id).first()
    if user_expense:
        db.session.delete(user_expense)
        db.session.commit()
        return {'status': 'DELETED'}, 204
    else:
        response_object = {
            'status': 'fail',
            'message': 'user expense not found',
        }
        return response_object, 409


def save_changes(data: UserExpense) -> UserExpense:
    db.session.add(data)
    db.session.commit()
    db.session.refresh(data)
    return data