# Imports
from flask import Blueprint, jsonify

bp = Blueprint('core', __name__, url_prefix='/core')


# Index Route
@bp.route('/', methods=['GET'])
def index():
    return jsonify({'msg': 'Hello, AegisScan!'})
