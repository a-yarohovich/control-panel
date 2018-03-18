from flask import Blueprint

blcountry_dict = Blueprint('country_dict', __name__)

from . import views
