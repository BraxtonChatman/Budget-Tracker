import os

class BaseConfig:
    SQL_ALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(BaseConfig):
    SQL_ALCHEMY_DATABASE_URI = 'sqlite:///instance/budget.db'
    SECRET_KEY = os.environ.get('SECRET_KEY', 'devkey')

class TestConfig(BaseConfig):
    SQL_ALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
    SECRET_KEY = 'testkey'

class ProdConfig(BaseConfig):
    SQL_ALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///instance/budget.db')
    SECRET_KEY = os.environ['SECRET_KEY']
