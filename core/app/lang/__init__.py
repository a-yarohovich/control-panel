from flask import Blueprint

lang_bl = Blueprint("lang", __name__)

from . import views
