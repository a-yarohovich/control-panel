from flask import Blueprint

serv_bl = Blueprint("services", __name__)

from . import views
