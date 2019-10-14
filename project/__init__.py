import os
import unittest

from flask import Flask
from flask import jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging
import requests
import json
logging.basicConfig(filename='app.log', level=logging.INFO)

from apscheduler.schedulers.background import BackgroundScheduler

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()

app_config = os.getenv('APP_SETTINGS')
app = Flask(__name__)
app.config.from_object(app_config)

db.init_app(app)
db.app = app
migrate.init_app(app, db)
ma.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)

CORS(app)

from project.api.planting_status.views import planting_status_blueprint
app.register_blueprint(planting_status_blueprint)


from project.api.planting_status.models import *
from project.api.irrigation.models import *
from project.api.illumination.models import *

from .api.planting_status.models import Machines, Plantings, Seedlings

def update_planting_photos():
    plantings = Plantings.query.filter_by(cycle_finished='false')
    
    for planting in plantings:
        machine = Machines.query.filter_by(id=planting.machine_id).first()
        if machine:
            rasp_ip = machine.raspberry_ip
            data={'raspberry_ip' : str(rasp_ip), 'planting_id' : planting.id}
            response = requests.post('%s/api/trigger_image_capture' % os.getenv('SVG_GATEWAY_BASE_URI'), json=data)
    
    db.session.close()
    return response

@app.route('/test_image_processing', methods=['GET'])
def test_image_processing():
    response = update_planting_photos()
    return jsonify(response.json()), response.status_code

cron = BackgroundScheduler()
cron.add_job(update_planting_photos, 'cron', minute=00, hour=10)

cron.start()

@app.cli.command('test')
def test():
    tests = unittest.TestLoader().discover('project/tests', pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1
