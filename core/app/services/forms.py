from flask_wtf import FlaskForm
from wtforms import *


class ServHandleForm(FlaskForm):
    submit_delete = SubmitField("Delete")
    submit_add = SubmitField("Create")
    submit_edit = SubmitField("Edit")


class ServWizard(FlaskForm):
    status_selector = SelectField("Status", coerce=int)
    desc = StringField("Description")
    serv_code = StringField("Service code", [validators.DataRequired(message="Field is required")])
    submit = SubmitField("Save service")
