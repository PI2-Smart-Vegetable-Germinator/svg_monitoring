from flask import Blueprint
from flask import jsonify

import datetime

from project import db
from .models import Machines, Plantings, Seedlings

planting_status_blueprint = Blueprint('planting_status', __name__)


@planting_status_blueprint.route('/api/ping/', methods=['GET'])
def ping():
    return jsonify({
        'response': 'pong!'
    }), 200

# ! se estiver ao contrário, trocar para pegar o ultimo !
@planting_status_blueprint.route('/api/current-info', methods=['GET'])
def get_current_info():
    plantings_data = Plantings.query.first()

    cycle_remaining_days = 0

    current_date = datetime.datetime.today()
    planting_time = current_date - plantings_data.planting_date

    if plantings_data.cycle_finished:
        cycle_remaining_days = -1
    else:
        cycle_remaining_days = (
            plantings_data.seedling.average_harvest_time - planting_time.days)

    return jsonify({
        'status': 'success',
        'data': {
            'planting_name': plantings_data.name,
            'planting_time': planting_time.days,
            'current_humidity': plantings_data.current_humidity,
            'current_temperature': plantings_data.current_temperature,
            'hours_backlit': plantings_data.hours_backlit,
            'cycle_remaining_days': cycle_remaining_days
        }
    }), 200


@planting_status_blueprint.route('/api/plantings-history/<machine_id>/', methods=['GET'])
def get_plantings_history(machine_id):

    return jsonify({
        'status': 'success',
        'data': {
            'plantings_history': [planting.to_json() for planting in Plantings.query.filter_by(machine_id=int(machine_id))]
        }
    }), 200
