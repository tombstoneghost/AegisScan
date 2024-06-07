"""
models.py
"""
from datetime import datetime
from flask_login import UserMixin
from aegis_scan import db, login_manager


class User(db.Model, UserMixin):
    """
    User Model
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.email}')"


@login_manager.user_loader
def load_user(user_id):
    """
    Load User based on his id
    """
    return User.query.get(int(user_id))
