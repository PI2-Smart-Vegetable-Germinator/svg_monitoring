from datetime import datetime

from flask import Blueprint
from flask import jsonify
from flask import request

from project import db
from project.api.planting_status.models import IlluminationsHistory, Machines, Plantings
from project.api.utils.constants import IlluminationModes


illumination_blueprint = Blueprint('illumination', __name__)


@illumination_blueprint.route('/api/start_illumination', methods=['POST'])
def start_illumination():
  post_data = request.get_json()

  planting_id = post_data.get('plantingId')
  planting = Plantings.query.filter_by(id=planting_id).first()

  # We can't start an illumination if the machine is already doing it.
  if planting and planting.machine.currently_irrigating:
    return jsonify({
        'success': False,
        'message': 'Is already being illuminated!'
    }), 403
  
  planting.machine.currently_backlit = True

  history_entry = IlluminationsHistory()
  history_entry.illumination_start_date = datetime.now()
  history_entry.illumination_mode = IlluminationModes.ManualIllumination.value
  history_entry.planting = planting
  
  db.session.add(planting)
  db.session.add(history_entry)

  db.session.commit()

  return jsonify({ 'success': True }), 201


@illumination_blueprint.route('/api/end_illumination', methods=['POST'])
def end_illumination():
    post_data = request.get_json()

    planting_id = post_data.get('plantingId')
    planting = Plantings.query.filter_by(id=planting_id).first()

    planting.machine.currently_backlit = False

    db.session.add(planting)
    db.session.commit()

    return jsonify({ 'success': True }), 201
