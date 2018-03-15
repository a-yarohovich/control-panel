import uuid
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or uuid.uuid4().bytes
    USER_ADMIN = os.environ.get('USER_ADMIN')
    # email server
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SENDER = os.environ.get('MAIL_USERNAME')
    # Rabbit
    RABBIT_USER = os.environ.get('RABBIT_USER')
    RABBIT_PASSWD = os.environ.get('RABBIT_PASSWD')
    RABBIT_HOST = os.environ.get('RABBIT_HOST')
    RABBIT_VHOST = '/'
    RABBIT_PORT = 5672
    PG_DATABASE_USER = os.environ.get('PG_DATABASE_USER')
    PG_DATABASE_PASSWORD = os.environ.get('PG_DATABASE_PASSWORD')
    PG_DATABASE_DB = 'mycapp'
    PG_DATABASE_HOST = 'localhost'

    @staticmethod
    def init_app(app):
        pass


class DelevopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass


config = {
    'develop': DelevopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DelevopmentConfig
}
