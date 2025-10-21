import datetime
from app.main import db
from app.main.model.user import User
from typing import Dict, Tuple


def save_new_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            created_at=datetime.datetime.utcnow(),
            fullname=data['fullname'],
            birthdate=data['birthdate'],
            phone=data['phone'],
            email=data['email']
        )
        return save_changes(new_user), 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists',
        }
        return response_object, 409


def update_user(id: int, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    user = db.session.query(User).filter_by(id=id).first()
    if user:
        user.fullname = data['fullname']
        user.birthdate = data['birthdate']
        user.sat_score = data['sat_score']
        user.graduation_score = data['graduation_score']
        user.phone = data['phone']
        user.email = data['email']
        db.session.commit()
        return user, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'User not found',
        }
        return response_object, 409


def get_all_users():
    return User.query.all()


def get_a_user(id):
    return db.session.query(User).filter(User.id == id).first()


def delete_user(id: int) -> Tuple[Dict[str, str], int]:
    user = db.session.query(User).filter(User.id == id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return {'status': 'DELETED'}, 204
    else:
        response_object = {
            'status': 'fail',
            'message': 'User not found',
        }
        return response_object, 409


def save_changes(data: User) -> User:
    db.session.add(data)
    db.session.commit()
    db.session.refresh(data)
    return data