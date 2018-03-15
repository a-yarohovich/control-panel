from flask import Blueprint

bl_create_users = Blueprint("create_users", __name__)

from . import views
