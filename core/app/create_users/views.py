from flask import render_template
from . import bl_create_users
from .forms import CreateUsersForm
from logger import logger

LOG = logger.LOG


@bl_create_users.route("/create_users", methods=["POST", "GET"])
def create_users_view():
    form = CreateUsersForm()
    if form.validate_on_submit():
        return render_template("create_users/create_users_view.html", form=form)
    else:
        return render_template("create_users/create_users_view.html", form=form)
