"""
User Routes
"""
# Imports
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from ..utils.validators import validate_url

bp = Blueprint('user', __name__, url_prefix='/api/user')


# Scan Target URL Route
@bp.route('/scan-target', methods=['POST'])
@jwt_required()
def scan_target():
    """
    Take Target Input and Scan the target
    """
    data = request.get_json()

    target = data.get('target')

    if not validate_url(target):
        return jsonify({'err': 'Invalid Target URL'})

    return jsonify({'msg': 'URL Submitted for Scanning.'})
