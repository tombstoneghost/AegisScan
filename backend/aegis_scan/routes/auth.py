"""
Authentication Routes
"""
import datetime
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user
from flask_jwt_extended import create_access_token, jwt_required
from aegis_scan.models.models import User
from aegis_scan import db, bcrypt



bp = Blueprint('auth', __name__, url_prefix='/api/auth')


# Register Route
@bp.route('/register', methods=['POST'])
def register():
    """
    Register a new User
    """
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already used"})
    
    if User.query.filter_by(username=username).first():
        return jsonify({'msg': 'Usernamer already used'})
    

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, email=email, password=hashed_password, role=role) # type: ignore
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"})


# Login Route
@bp.route('/login', methods=['POST'])
def login():
    """
    User Login
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user, remember=True)
        access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(hours=12))
        return jsonify({'msg': 'Login Successful', 'access_token': access_token})
    
    return jsonify({'msg': 'Invalid Credentials'})


# Logout Route
@bp.route('/logout')
@jwt_required()
def logout():
    """
    User Logout
    """
    logout_user()

    return jsonify({'msg': 'Logout Successful'})
