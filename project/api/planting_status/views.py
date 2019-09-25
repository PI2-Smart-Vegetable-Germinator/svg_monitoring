from flask import Blueprint
from flask import jsonify


planting_status_blueprint = Blueprint('planting_status', __name__)


@planting_status_blueprint.route('/api/ping', methods=['GET'])
def ping():
    return jsonify({
        'response': 'pong!'
    }), 200
