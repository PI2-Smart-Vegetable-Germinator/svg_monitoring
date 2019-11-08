from flask import Blueprint
from flask import jsonify

import sys
import os
import requests

import datetime

from project import db
from project.api.utils.notifications import NotificationSender
from .models import Machines, Plantings, Seedlings
from flask import request

planting_status_blueprint = Blueprint('planting_status', __name__)
from project import db
from .models import Machines, Plantings, Seedlings

from .schemas import PlantingsSchema
from .schemas import PlantingInfoSchema

@planting_status_blueprint.route('/api/ping', methods=['GET'])
def ping():
    return jsonify({
        'response': 'pong!'
    }), 200

@planting_status_blueprint.route('/api/planting', methods=['POST'])
def start_planting():
    post_data = request.get_json()
    planting = Plantings()

    planting.planting_date = datetime.datetime.now()
    planting.seedling_id = post_data.get('seedlingId')
    planting.machine_id = post_data.get('machineId')
    planting.current_humidity = post_data.get('currentHumidity')
    planting.current_temperature = post_data.get('currentTemperature')
    planting.sprouted_seedlings = 0
    planting.hours_backlit = 0
    planting.name = "Plantio #"

    db.session.add(planting)
    db.session.flush()

    planting.machine.planting_active = True

    planting.name += str(planting.id)

    db.session.commit()

    return jsonify({
        'success': True,
        'plantingId': planting.id
    }), 201

@planting_status_blueprint.route('/api/end_planting', methods=['POST'])
def end_planting():
    post_data = request.get_json()

    planting = Plantings.query.filter_by(id=post_data.get('plantingId')).first()

    planting.cycle_ending_date = datetime.datetime.now()
    planting.cycle_finished = True
    planting.machine.planting_active = False

    db.session.add(planting)
    db.session.commit()

    return jsonify({
        'success': True
    }), 201

# ! se estiver ao contrário, trocar para pegar o ultimo !
@planting_status_blueprint.route('/api/current-info', methods=['GET'])
def get_current_info():
    plantings_data = Plantings.query.order_by(Plantings.id.desc()).first()

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

@planting_status_blueprint.route('/api/update_planting_info', methods=['POST'])
def update_current_info():
    post_data = request.get_json()

    schema = PlantingInfoSchema()

    planting = Plantings.query.filter_by(id=post_data.get('plantingId')).first()

    planting_update = schema.load(post_data, instance=planting, partial=True)

    db.session.add(planting_update)
    db.session.commit()

    if planting.current_humidity <= planting.seedling.humidity_threshold:
        auth_response = requests.get('%s/api/users' % os.getenv('SVG_GATEWAY_BASE_URI'))

        if auth_response.status_code == 200:
            auth_response_content = auth_response.json()
            users = auth_response_content['users']

            device_ids = [
                user['deviceId']
                for user in users
                if user['machineId'] == planting.machine_id and user['deviceId']
            ]

            sender = NotificationSender()
            notification = {
                'title': 'Umidade baixa!',
                'body': 'A umidade em sua SVG está baixa! Considere ativar a irrigação.'
            }

            try:
                for device_id in device_ids:
                    print(device_id)
                    sender.send_message(device_id, notification)
            except Exception as e:
                print(str(e), file=sys.stderr)

    return jsonify({
        'success': True
    }), 201


@planting_status_blueprint.route('/api/plantings-history/<machine_id>/', methods=['GET'])
def get_plantings_history(machine_id):

    schema = PlantingsSchema()

    plantings = Plantings.query.filter_by(machine_id=int(machine_id)).order_by(Plantings.id.desc()).all()

    return jsonify({
        'status': 'success',
        'data': {
            'plantings_history': [schema.dump(planting) for planting in plantings]
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

    planting = Plantings.query.filter_by(id=planting_id).first()
    planting.sprouted_seedlings = sprouted_seedlings
    db.session.add(planting)
    db.session.commit()
    db.session.close()

    return jsonify({
        'success' : True,
        'sprouted_seedlings' : sprouted_seedlings,
        'green_percentage' : green_percentage,
        'planting_id' : planting_id}), 200
