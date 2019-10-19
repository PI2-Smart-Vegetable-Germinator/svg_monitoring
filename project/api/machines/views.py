from flask import Blueprint
from flask import jsonify
from flask import request

machines_blueprint = Blueprint("machines", __name__)
from project import db
from project.api.planting_status.models import Machines

from .schemas import CreateMachineSchema
from .schemas import UpdateMachineSchema


@machines_blueprint.route('/api/machine', methods=['POST'])
def create_or_update_machine():
    post_data = request.get_json()

    if not post_data.get('id'):
        schema = CreateMachineSchema()
        
        machine = schema.load(post_data, partial=True)
        db.session.add(machine)
        db.session.commit()

        return jsonify({
            'success': True,
            'machineId': machine.id
        }), 201
    
    schema = UpdateMachineSchema()
    machine = Machines.query.filter_by(id=post_data['id']).first()
    machine_update = schema.load(post_data, instance=machine, partial=True)
    db.session.add(machine_update)
    db.session.commit()

    return jsonify({
        'success': True
    }), 201


@machines_blueprint.route('/api/confirm_pairing', methods=['POST'])
def confirm_pairing():
    post_data = request.get_json()

    pincode = post_data['pincode']

    machine = Machines.query.filter_by(pincode=pincode).first()

    if machine is None:
        return jsonify({
            'success': False,
            'message': 'Invalid pincode!'
        }), 404

    return jsonify({
        'success': True,
        'machineId': machine.id
    }), 201
