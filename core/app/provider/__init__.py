from flask import Blueprint

provider_bl = Blueprint("provider", __name__)

from . import views
