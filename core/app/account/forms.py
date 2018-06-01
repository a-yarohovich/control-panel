from flask_wtf import FlaskForm
from wtforms import *
from wtforms.fields.html5 import DateField as dt


class AccHandleForm(FlaskForm):
    submit_delete = SubmitField("Delete")
    submit_add = SubmitField("Create")
    submit_edit = SubmitField("Edit")


class AccWizard(FlaskForm):
    code = StringField(
        "Code",
        validators=[validators.DataRequired("Field is required"), validators.Length(1, 64)]
    )
    Paytype = SelectField("Pay type", coerce=int)
    start_date = dt("Start date", format="%Y-%m-%d")
    close_date = dt("Close date", format="%Y-%m-%d")
    lang = SelectField("Lang", coerce=int)
    status = IntegerField("Status")
    blockcode = IntegerField("Block code")
    balance = DecimalField("Balance")
    currency = SelectField("Currency", coerce=int)
    submit = SubmitField("Save")
