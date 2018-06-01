from flask import Blueprint

lang_bl = Blueprint("acc", __name__)

from . import views
