import pprint
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from config import config
from logger import logger
from .db_adapter import MyPgConnection

LOG = logger.LOG
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db_conn = MyPgConnection()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    db_conn.init(
        dbname=app.config["PG_DATABASE_DB"],
        user=app.config["PG_DATABASE_USER"],
        passwd=app.config["PG_DATABASE_PASSWORD"],
        host=app.config["PG_DATABASE_HOST"]
    )
    LOG.info("Print config:{}".format(pprint.pformat(app.config)))
    from .cdr import cdr
    from .create_users import bl_create_users
    from .country_dict import blcountry_dict
    from .main import main
    from .auth import auth
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(cdr, url_prefix='/cdr')
    app.register_blueprint(blcountry_dict, url_prefix='/country_dict')
    app.register_blueprint(bl_create_users, url_prefix="/create_users")
    return app
