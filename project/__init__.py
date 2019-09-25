import os
import unittest

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()

app_config = os.getenv('APP_SETTINGS')
app = Flask(__name__)
app.config.from_object(app_config)

db.init_app(app)
ma.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)

CORS(app)

from project.api.planting_status.views import planting_status_blueprint
app.register_blueprint(planting_status_blueprint)


@app.cli.command('test')
def test():
    tests = unittest.TestLoader().discover('project/tests', pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1
