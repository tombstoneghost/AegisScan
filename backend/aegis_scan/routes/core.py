"""
Core Routes
"""
# Imports
from flask import Blueprint, jsonify

bp = Blueprint('core', __name__, url_prefix='/api/core')


# Index Route
@bp.route('/', methods=['GET'])
def index():
    """Core Index"""
    
    return jsonify({'msg': 'Hello, AegisScan!'})
