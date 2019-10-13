from flask import Blueprint
from flask import jsonify

import datetime

from project import db
from .models import Machines, Plantings, Seedlings

planting_status_blueprint = Blueprint('planting_status', __name__)
from .models import Machines, Plantings, Seedlings



@planting_status_blueprint.route('/api/ping', methods=['GET'])
def ping():
    return jsonify({
        'response': 'pong!'
    }), 200


@planting_status_blueprint.route('/api/planting-time', methods=['GET'])
def get_planting_time():
    plantings_data = Plantings.query.first()

    current_date = datetime.datetime.today()
    planting_time = current_date - plantings_data.planting_date

    return jsonify({
        'status': 'success',
        'data': {
            'planting_name': plantings_data.name,
            'planting_time': planting_time.days
        }
    }), 200

@planting_status_blueprint.route('/api/current-info', methods=['GET'])
def get_current_info():
    plantings_data = Plantings.query.first()

    return jsonify({
        'status': 'success',
        'data': {
            'current_humidity': plantings_data.current_humidity,
            'current_temperature': plantings_data.current_temperature,
            'hours_backlit': plantings_data.hours_backlit
        }
    }), 200
@planting_status_blueprint.route('/api/get_id', methods=['GET'])
def get_id():
    machines = Machines.query.first()

    return jsonify({
        'response': machines.id
    }), 200

@planting_status_blueprint.route('/api/image_processing_results', methods=['POST'])
def image_processing_results():
    request_data = request.get_json()
    planting_id = request_data['planting_id']
    sprouted_seedlings = request_data['sprouted_seedlings']
    green_percentage = request_data['green_percentage']

    response = {
        'planting_id' : planting_id,
        'sprouted_seedlings' : sprouted_seedlings,
        'green_percentage' : green_percentage
    }

    print(response)

    return jsonify(response.json()), 200
