import datetime
import os

class BaseConfig:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)


class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    JWT_SECRET_KEY = os.getenv('SECRET_KEY')

class TestConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI')
    JWT_SECRET_KEY = 'super secret test key wooo'

