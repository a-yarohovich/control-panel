from flask import Blueprint

cdr = Blueprint('cdr', __name__)

from . import views
