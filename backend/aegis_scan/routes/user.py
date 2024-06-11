"""
User Routes
"""
# Imports
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from ..models.models import Scan
from ..services.scanner.scanner import Scanner

bp = Blueprint('user', __name__, url_prefix='/api/user')
scanner = Scanner()


# Scan Target URL Route
@bp.route('/scan-target', methods=['POST'])
@jwt_required()
def scan_target():
    """
    Take Target Input and Scan the target
    """
    data = request.get_json()

    target = data.get('target')

    user_id = get_jwt_identity()

    scanner.init_scanner(target=target, user_id=user_id)

    return jsonify({'msg': 'URL Submitted for Scanning.'})


# Get all running scans
@bp.route('/scans/running', methods=['GET'])
@jwt_required()
def scan_running():
    """
    Returns all the running scans
    """
    user_id = get_jwt_identity()

    result = Scan.query.filter_by(user_id=user_id).filter(Scan.status != 'Completed').all() # type: ignore

    running_scans = []

    for r in result:
        obj = r.__dict__

        running_scans.append({'scan_id': obj['scan_id'], 'scan_type': obj['scan_type'], 'status': obj['status'], 'url': obj['url'], 'id': obj['id']})

    return {'result': running_scans}


# Get running scan status
@bp.route('/scan/status/<string:scan_id>', methods=['GET'])
@jwt_required()
def scan_status(scan_id):
    """
    Returns the status of the running scan
    """
    user_id = get_jwt_identity()

    result = Scan.query.filter_by(user_id=user_id).filter_by(scan_id=scan_id.upper()).first()

    spider_scan_id = str(result.__dict__.get('spider_scan_id'))

    status = scanner.get_spider_status(scan_id=spider_scan_id, scan=result)

    return {'result': status}
