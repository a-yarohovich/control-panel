from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField as dt
from wtforms import *


class CdrFilterForm(FlaskForm):
    from_date = dt('From date', format='%Y-%m-%d')
    to_date = dt('To date', format='%Y-%m-%d')
    submit = SubmitField("Display CDRs")
