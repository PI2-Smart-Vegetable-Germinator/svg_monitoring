from datetime import datetime

from flask import Blueprint
from flask import jsonify
from flask import request

import requests
import os

from project import db
from project.api.planting_status.models import IrrigationsHistory
from project.api.planting_status.models import Machines
from project.api.planting_status.models import Plantings
from project.api.utils.constants import IrrigationModes
from project.api.utils.notifications import NotificationSender

irrigation_blueprint = Blueprint('irrigation', __name__)


@irrigation_blueprint.route('/api/start_irrigation', methods=['POST'])
def start_irrigation():
    post_data = request.get_json()

    planting_id = post_data.get('plantingId')
    planting = Plantings.query.filter_by(id=planting_id).first()

    # We can't start an irrigation if the machine is already doing it.
    if planting and planting.machine.currently_irrigating:
        return jsonify({
            'success': False,
            'message': 'Irrigation already underway!'
        }), 403
    
    planting.machine.currently_irrigating = True

    history_entry = IrrigationsHistory()
    history_entry.irrigation_date = datetime.now()
    history_entry.irrigation_mode = IrrigationModes.ManualIrrigation.value
    history_entry.planting = planting
    
    db.session.add(planting)
    db.session.add(history_entry)

    db.session.commit()

    return jsonify({
        'success': True,
    }), 201


@irrigation_blueprint.route('/api/end_irrigation', methods=['POST'])
def end_irrigation():
    post_data = request.get_json()

    planting_id = post_data.get('plantingId')
    planting = Plantings.query.filter_by(id=planting_id).first()

    planting.machine.currently_irrigating = False

    db.session.add(planting)
    db.session.commit()

    auth_response = requests.get('%s/api/users' % os.getenv('SVG_GATEWAY_BASE_URI'))
    auth_response_content = auth_response.json()
    users = auth_response_content['users']

    device_ids = [
        user['deviceId']
        for user in users
        if user['machineId'] == planting.machine_id and user['deviceId']
    ]

    sender = NotificationSender()
    notification = {
        'title': 'Irrigação terminada',
        'body': 'Mudas irrigadas com sucesso!',
        'dataContent': {
            'code': 'SVG_IRRIGATION_SUCCESS',
            'click_action': 'FLUTTER_NOTIFICATION_CLICK'
        }
    }

    try:
        for device_id in device_ids:
            sender.send_message(device_id, notification)
    except Exception as e:
        print(str(e), file=sys.stderr)

    return jsonify({
        'success': True
    }), 201


@irrigation_blueprint.route('/api/switch_smart_irrigation/<machine_id>', methods=['POST'])
def switch_smart_irrigation(machine_id):
    machine_data = Machines.query.filter_by(id=machine_id).first()

    machine_data.smart_irrigation_enabled = (not machine_data.smart_irrigation_enabled)

    db.session.add(machine_data)
    db.session.commit()

    print('\n\n inferno')
    print(machine_data.smart_irrigation_enabled)

    return jsonify({
        'success': True,
        'smart_irrigation_status': machine_data.smart_irrigation_enabled
    }), 201


@irrigation_blueprint.route('/api/get_smart_irrigation_status/<machine_id>', methods=['GET'])
def get_smart_irrigation_status(machine_id):
    machine_data = Machines.query.filter_by(id=machine_id).first()

    return jsonify({
        'success': True,
        'smart_irrigation_status': machine_data.smart_irrigation_enabled
    }), 201


