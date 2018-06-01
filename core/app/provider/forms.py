from flask_wtf import FlaskForm
from wtforms import *
from wtforms.fields.html5 import DateField as dt


class ProvHandleForm(FlaskForm):
    submit_delete = SubmitField("Delete")
    submit_add = SubmitField("Create")
    submit_edit = SubmitField("Edit")


class ProvWizard(FlaskForm):
    status_selector = SelectField("Status", coerce=int)
    prov_code = StringField("Code", [validators.DataRequired(message="Field is required")])
    desc = StringField("Description")
    from_date = dt("Start date", format="%Y-%m-%d")
    to_date = dt("End date", format="%Y-%m-%d")
    submit = SubmitField("Save")
