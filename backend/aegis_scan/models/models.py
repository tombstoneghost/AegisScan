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
    scan = db.relationship('Scan', backref='user', lazy=True)

    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.email}')"

@login_manager.user_loader
def load_user(user_id):
    """
    Load User based on his id
    """
    return User.query.get(int(user_id))


class Scan(db.Model):
    """
    Model to store all scans
    """
    id = db.Column(db.Integer, primary_key=True)
    scan_id = db.Column(db.String(32), nullable=False, unique=True)
    url = db.Column(db.String(512), nullable=False)
    scan_type = db.Column(db.String(50), nullable=False)
    application_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    result = db.Column(db.Text, nullable=True)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    end_time = db.Column(db.DateTime, nullable=True)
    duration = db.Column(db.Float, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_scan_user'), nullable=False)
    spider_scan_id = db.Column(db.String(32), nullable=True)
    active_scan_id = db.Column(db.Text, nullable=True)

    def __init__(self, scan_id, url, scan_type, application_type, target_type, status, user_id, spider_result=None, active_result=None, end_time=None, duration=None) -> None:
        self.scan_id = scan_id
        self.url = url
        self.scan_type = scan_type
        self.application_type = application_type
        self.target_type = target_type
        self.status = status
        self.user_id = user_id
        self.spider_result = spider_result
        self.active_result = active_result
        self.end_time = end_time
        self.duration = duration

    def to_dict(self) -> dict:
        return {
            "scan_id": self.scan_id,
            "url": self.url,
            "scan_type": self.scan_type,
            "application_type": self.application_type,
            "status": self.status,
            "result": self.result,
            "start_time": self.start_time.strftime('%Y-%m-%d %H:%M:%S') if self.start_time else "NA", 
            "end_time": self.end_time.strftime('%Y-%m-%d %H:%M:%S') if self.end_time else "NA",
            "duration": self.duration if self.duration else "NA",
            "user_id": self.user_id,
            "spider_scan_id": self.spider_scan_id if self.spider_scan_id else "NA",
            "active_scan_id": self.active_scan_id if self.active_scan_id else "NA"
        }

