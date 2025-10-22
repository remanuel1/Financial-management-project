import datetime
from app.main import db
from app.main.model.user import User
from app.main.model.user_expense import UserExpense
from typing import Dict, Tuple
from app.main.util.fps import get_paginated


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


def get_all_expenses(user_id, start_date, end_date, store_name, category,
                     orderby_field, orderby_direction, page, count):
    """
    Get all user expenses with optional filters and pagination.
    """

    fields = [
        ("ue.id", "id"),
        ("ue.created_at", "created_at"),
        ("ue.user_id", "user_id"),
        ("ue.date", "date"),
        ("ue.store_name", "store_name"),
        #("ue.sum", "sum"),
        ("ue.category", "category")
    ]

    from_str = "FROM user_expense ue"

    where_str = """WHERE (1=1)"""

    if user_id is not None:
        where_str += " AND ue.user_id = :user_id"
        #params["user_id"] = user_id

    if start_date is not None and end_date is not None:
        where_str += " AND ue.date BETWEEN :start_date AND :end_date"
        #params["start_date"] = start_date
        #params["end_date"] = end_date

    if store_name is not None:
        where_str += " AND LOWER(ue.store_name) LIKE CONCAT('%', :store_name, '%')"
        #params["store_name"] = store_name.lower()

    if category is not None:
        where_str += " AND ue.category = :category"
        #params["category"] = category

    params = {"user_id": user_id, "start_date": start_date, "end_date": end_date, "store_name": store_name, "category": category}

    return get_paginated(fields=fields,
                         from_str=from_str,
                         where_str=where_str,
                         orderby_field=orderby_field,
                         orderby_direction=orderby_direction,
                         page=page,
                         count=count,
                         params=params)


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