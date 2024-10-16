"""
User Routes
"""
# Imports
import json
from sqlalchemy import not_
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from ..models.models import Scan
from ..services.scanner.scanner import Scanner
from aegis_scan import db

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
    scan_type = data.get('scan_type')

    user_id = get_jwt_identity()

    scanner.init_scanner(target=target, user_id=user_id, scan_type=scan_type)

    return jsonify({'msg': 'URL Submitted for Scanning.'})


# Get all running scans
@bp.route('/scans/running', methods=['GET'])
@jwt_required()
def scan_running():
    """
    Returns all the running scans
    """
    user_id = get_jwt_identity()

    result = Scan.query.filter_by(user_id=user_id).filter(not_(Scan.status.like('%Completed%'))).filter(not_(Scan.status.like('%Failed%'))).all() # type: ignore

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

    status, progress = scanner.get_scan_status(scan_id=spider_scan_id, scan=result)

    print("Progress", progress)

    return {'result': status, 'progress': progress}

# Get all scans
@bp.route('/scans/all', methods=['GET'])
@jwt_required()
def scans_all():
    """
    Returns all the scans
    """
    user_id = get_jwt_identity()

    result = Scan.query.filter_by(user_id=user_id).all() # type: ignore

    all_scans = []

    for r in result:
        obj = r.__dict__

        all_scans.append({'scan_id': obj['scan_id'], 'scan_type': obj['scan_type'], 'status': obj['status'], 'url': obj['url'], 'id': obj['id']})

    all_scans = all_scans[::-1]

    return {'result': all_scans}


# Get Scan Results
@bp.route('/scan/results/<string:scan_id>', methods=['GET'])
@jwt_required()
def scan_result(scan_id):
    """
    Returns the scan results
    """
    user_id = get_jwt_identity()

    result = Scan.query.filter_by(user_id=user_id).filter_by(scan_id=scan_id.upper()).first()

    result_json = result.to_dict()

    return {'result': result_json}


# Delete a Scan
@bp.route('/scan/delete/<string:scan_id>', methods=['GET'])
@jwt_required()
def scan_delete(scan_id):
    """
    Deletes the Scan
    """
    
    scan_item = Scan.query.filter_by(scan_id=scan_id.upper()).first()

    if scan_item:
        db.session.delete(scan_item)
        db.session.commit()

    return {"result": "Scan Deleted Successfully"}
