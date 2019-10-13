from flask import Blueprint
from flask import jsonify

import datetime

from project import db
from .models import Machines, Plantings, Seedlings

planting_status_blueprint = Blueprint('planting_status', __name__)


@planting_status_blueprint.route('/api/ping', methods=['GET'])
def ping():
    return jsonify({
        'response': 'pong!'
    }), 200


@planting_status_blueprint.route('/api/current-info', methods=['GET'])
def get_current_info():
    plantings_data = Plantings.query.first()

    harvest_time = 0

    current_date = datetime.datetime.today()
    planting_time = current_date - plantings_data.planting_date

    if plantings_data.cycle_finished:
        harvest_time = -1
    else:
        harvest_time = (plantings_data.seedling.average_harvest_time - planting_time.days)

    return jsonify({
        'status': 'success',
        'data': {
            'planting_name': plantings_data.name,
            'planting_time': planting_time.days,
            'current_humidity': plantings_data.current_humidity,
            'current_temperature': plantings_data.current_temperature,
            'hours_backlit': plantings_data.hours_backlit,
            'cycle_remaining_days': harvest_time
        }
    }), 200
