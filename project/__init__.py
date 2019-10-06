import os
import unittest

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging
import requests
logging.basicConfig(filename='app.log', level=logging.INFO)

from apscheduler.schedulers.background import BackgroundScheduler

def update_planting_photos():
    response = requests.get('%s/api/ping' % os.getenv('SVG_GATEWAY_BASE_URI'))
    print(response)

cron = BackgroundScheduler()
cron.add_job(update_planting_photos, 'cron', minute=00, hour=10)

cron.start()

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()

app_config = os.getenv('APP_SETTINGS')
app = Flask(__name__)
app.config.from_object(app_config)

db.init_app(app)
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

@app.cli.command('test')
def test():
    tests = unittest.TestLoader().discover('project/tests', pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1
